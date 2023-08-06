/* For hash functions */
CREATE EXTENSION IF NOT EXISTS pgcrypto;


/* Extract hash type of message from data */
CREATE OR REPLACE FUNCTION hash_type(data bytea) RETURNS hash_type AS $$
  SELECT CASE get_byte(data, 0) & 127
    WHEN 1 THEN 'sha256'
    WHEN 2 THEN 'sha384'
    WHEN 3 THEN 'sha512'
  END::hash_type;
$$ LANGUAGE sql IMMUTABLE;


/* Extract metadata flag of message from data */
CREATE OR REPLACE FUNCTION has_metadata(data bytea) RETURNS bool AS $$
  SELECT get_byte(data, 0) & 128 > 0;
$$ LANGUAGE sql IMMUTABLE;


/* Extract message body from data */
CREATE OR REPLACE FUNCTION message_body(data bytea) RETURNS bytea AS $$
  SELECT substring(data FROM 2);
$$ LANGUAGE sql IMMUTABLE;


/* Tag a message body with a particular hash type */
CREATE OR REPLACE FUNCTION tag_message(hash_type hash_type, has_metadata bool, message_body bytea) RETURNS bytea AS $$
  SELECT set_bit(
      chr(CASE hash_type
          WHEN 'sha256' THEN 1
          WHEN 'sha384' THEN 2
          WHEN 'sha512' THEN 3
      END)::bytea,
      7,  /* set most significant bit */
      has_metadata::int
  ) || message_body;
$$ LANGUAGE sql IMMUTABLE;


/* Hashing gotchas: Hashing Text fields works differently than hashing bytea.
 * Always cast to bytea before passing to digest().
 *
 * Non-gotcha: typeof(bytea || text) and typeof(text || byeta) are both bytea.
 */
CREATE OR REPLACE FUNCTION message_hash(topic bytea, data bytea) RETURNS bytea AS $$
  SELECT chr(get_byte(data, 0) & 127)::bytea || digest(coalesce(topic, ''::bytea) || data, hash_type(data)::text);
$$ LANGUAGE sql IMMUTABLE;


CREATE TABLE IF NOT EXISTS message(
  id bytea,
  topic_serial bigint,
  topic bytea,
  data bytea NOT NULL,
  signature bytea,
  CONSTRAINT message_check_topic_serialized CHECK ((topic_serial IS NOT NULL) = (topic IS NOT NULL)),
  CONSTRAINT message_check_topic_null_or_non_empty CHECK (topic IS NULL OR length(topic) > 0)
);
CREATE UNIQUE INDEX IF NOT EXISTS message_ix_hashid ON message(id);
CREATE UNIQUE INDEX IF NOT EXISTS message_ix_topic ON message(topic, topic_serial) WHERE topic IS NOT NULL;
/* Drop and re-create message_check_hash_type, which is free since it is a NOT VALID constraint. */
ALTER TABLE message DROP CONSTRAINT IF EXISTS message_check_hash_type;
ALTER TABLE message ADD CONSTRAINT message_check_hash_type
  CHECK (hash_type(data) IS NOT NULL AND hash_type(data) >= 'sha256') NOT VALID;

/* The hash of the messages will be stored as a trigger-computed column materialized
 * on the table itself so that they can be selected out. In the future, index-only scans
 * may be able to select computed columns from indexes that do not contain the columns
 * passed to the function. Currently this is not the case and selecting the computed
 * hash of a message will always recompute the hash from scratch, which is very undesirable
 * for large messages.
 */
CREATE OR REPLACE FUNCTION tgfn_hash_message() RETURNS TRIGGER AS $$
BEGIN
  NEW.id = message_hash(NEW.topic, NEW.data);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tg_hash_message ON message;
CREATE TRIGGER tg_hash_message
  BEFORE INSERT OR UPDATE ON message
  FOR EACH ROW EXECUTE PROCEDURE tgfn_hash_message();


CREATE TABLE IF NOT EXISTS topic_choked(
  topic bytea NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS topic_choked_ix ON topic_choked(topic);



/* convert last 8 bytes of message_id to a bigint */
CREATE OR REPLACE FUNCTION message_id_to_lock(message_id bytea) RETURNS bigint AS $$
  SELECT ('x' || encode(substring(message_id from length(message_id) - 7), 'hex'))::bit(64)::bigint;
$$ LANGUAGE sql IMMUTABLE;


/* Message posting function. Sequential calls with the same arguments will produce the same changes
 * in the database as only one call, but will return different values indicating what actually
 * changed on any particular call.
 *
 * Returns the first of the following text values describing the result:
 *   failure_disallowed_hash_type: posting new messages with this hashtype is disallowed
 *   nochange_message_exists: message already exists
 *   success: message successfully added
 *
 * Note: Does nothing to check the signature, merely storing that data as-is.
 */
/* Same as above, but post tagged message data directly */
CREATE OR REPLACE FUNCTION post_message_raw(
  _topic bytea,
  _data bytea,
  _signature bytea,
  out status text,
  out message_id bytea
) RETURNS RECORD AS $$
DECLARE
  next_serial bigint = NULL;
  err_info text;
BEGIN
  IF _topic IS NOT NULL THEN
    /* acquire lock for topic to ensure topic_serial is serialized */
    PERFORM pg_advisory_xact_lock(message_id_to_lock(_topic));

    SELECT coalesce(max(topic_serial), 0) + 1 FROM message WHERE topic = _topic INTO next_serial;
  END IF;

  BEGIN
    INSERT INTO message(topic, topic_serial, data, signature)
      VALUES (
        _topic,
        next_serial,
        _data,
        _signature
      ) RETURNING id INTO message_id;
  EXCEPTION
    WHEN unique_violation THEN
      GET STACKED DIAGNOSTICS err_info = CONSTRAINT_NAME;
      CASE err_info
        WHEN 'message_ix_hashid' THEN
          status := 'nochange_message_exists';
          RETURN;
        ELSE
          RAISE;  /* re-raise */
      END CASE;
    WHEN check_violation THEN
      GET STACKED DIAGNOSTICS err_info = CONSTRAINT_NAME;
      CASE err_info
        WHEN 'message_check_hash_type' THEN
          status := 'failure_disallowed_hash_type';
          RETURN;
        ELSE
          RAISE;  /* re-raise */
      END CASE;
  END;

  status := 'success';
  RETURN;
END;
$$ LANGUAGE plpgsql VOLATILE;

CREATE OR REPLACE FUNCTION post_message(
  _topic bytea,
  _hash_type hash_type,
  _has_metadata bool,
  _message_body bytea,
  _signature bytea,
  out status text,
  out message_id bytea
) RETURNS RECORD AS $$
  SELECT post_message_raw(_topic, tag_message(_hash_type, _has_metadata, _message_body), _signature);
$$ LANGUAGE sql VOLATILE;



/* Returns the number of messages posted on a topic, including closing message.
 *
 * If integrity is maintained, this function should always return the same value as
 * (SELECT count(*) FROM message WHERE topic = _topic), but in sub-linear time --
 * assuming that no messages have been deleted or stored elsewhere.
 */
CREATE OR REPLACE FUNCTION topic_size(
  _topic bytea
) RETURNS bigint AS $$
  SELECT coalesce(max(topic_serial), 0) FROM message WHERE topic = _topic;
$$ LANGUAGE sql VOLATILE;


CREATE OR REPLACE FUNCTION topic_set_choke(_topic bytea, _choke boolean DEFAULT true) RETURNS VOID AS $$
BEGIN
  IF _choke THEN
    INSERT INTO topic_choked(topic) VALUES (_topic) ON CONFLICT DO NOTHING;
  ELSE
    DELETE FROM topic_choked WHERE topic = _topic;
  END IF;
END;
$$ LANGUAGE plpgsql VOLATILE;


CREATE OR REPLACE FUNCTION topic_is_choked(_topic bytea) RETURNS boolean AS $$
  SELECT EXISTS (SELECT * FROM topic_choked WHERE topic = _topic);
$$ LANGUAGE sql VOLATILE;

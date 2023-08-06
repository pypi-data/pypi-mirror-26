START TRANSACTION;

DO $$
DECLARE
  data bytea;
  TEST_TOPIC CONSTANT bytea = '\000test_topic';
BEGIN
  ASSERT NOT EXISTS (SELECT * FROM message WHERE id = TEST_TOPIC OR topic = TEST_TOPIC),
    'test data should not exist yet';

  ASSERT digest(''::bytea, 'sha256') = '\xe3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    'sha256 works as expected';

  ASSERT message_hash('', '\001') = '\001' || digest('\001'::bytea, 'sha256'),
    'sha256 hash id of empty message';
  ASSERT message_hash('', '\002') = '\002' || digest('\002'::bytea, 'sha384'),
    'sha384 hash id of empty message';
  ASSERT message_hash('', '\003') = '\003' || digest('\003'::bytea, 'sha512'),
    'sha512 hash id of empty message';
  ASSERT message_hash('test', '\001') = '\001' || digest('test\001'::bytea, 'sha256'),
    'sha256 hash id of test all in topic';
  ASSERT message_hash('', '\001test') = '\001' || digest('\001test'::bytea, 'sha256'),
    'sha256 hash id of test all in data';
  ASSERT message_hash(null, '\001test') = '\001' || digest('\001test'::bytea, 'sha256'),
    'sha256 hash id of test all in data with null topic';
  ASSERT message_hash('te', '\001st') = '\001' || digest('te\001st'::bytea, 'sha256'),
    'sha256 hash id of test split across both';
  ASSERT message_hash('te', '\002st') = '\002' || digest('te\002st'::bytea, 'sha384'),
    'sha384 hash id of test split across both';
  ASSERT message_hash('te', '\003st') = '\003' || digest('te\003st'::bytea, 'sha512'),
    'sha512 hash id of test split across both';
  ASSERT message_hash('te', '\201st') = '\001' || digest('te\201st'::bytea, 'sha256'),
    'sha256 hash id of test split across both with metadata';
  ASSERT message_hash('te', '\202st') = '\002' || digest('te\202st'::bytea, 'sha384'),
    'sha384 hash id of test split across both with metadata';
  ASSERT message_hash('te', '\203st') = '\003' || digest('te\203st'::bytea, 'sha512'),
    'sha512 hash id of test split across both with metadata';
  ASSERT message_hash('does not matter', 'omg') IS NULL,
    'hash of message with invalid hash type';

  data := tag_message('sha256', false, 'things');
  ASSERT hash_type(data) = 'sha256', 'tag_message test hash type 1';
  ASSERT has_metadata(data) = false, 'tag_message test has metadata 1';
  ASSERT message_body(data) = 'things', 'tag_message test body 1';
  data := tag_message('sha512', true, 'additional things');
  ASSERT hash_type(data) = 'sha512', 'tag_message test hash type 2';
  ASSERT has_metadata(data) = true, 'tag_message test has metadata 2';
  ASSERT message_body(data) = 'additional things', 'tag_message test body 2';

  ASSERT post_message_raw(TEST_TOPIC, 'invalid hash type', 'signature') =
         ROW('failure_disallowed_hash_type'::text, null::bytea),
    'posting a message with invalid hash type should fail';

  ASSERT topic_size(TEST_TOPIC) = 0,
    'size of empty topic should be zero';
  ASSERT post_message(TEST_TOPIC, 'sha256', false, 'information', 'John Hancock') =
         ROW('success'::text, '\001' || digest(TEST_TOPIC || '\001information'::bytea, 'sha256')),
    'posting message should succeed';
  ASSERT topic_size(TEST_TOPIC) = 1,
    'topic should now have size 1';
  ASSERT post_message(TEST_TOPIC, 'sha256', false, 'information', 'John Hancock') =
         ROW('nochange_message_exists'::text, null::bytea),
    'reposting same message should return nochange';
  ASSERT post_message(TEST_TOPIC, 'sha256', false, 'information', 'Ben Franklin') =
         ROW('nochange_message_exists'::text, null::bytea),
    'different signature should not affect message identity';
  ASSERT post_message(TEST_TOPIC, 'sha256', true, 'information', 'Ben Franklin') =
         ROW('success'::text, '\001' || digest(TEST_TOPIC || '\201information'::bytea, 'sha256')),
    'setting has_metadata flag should affect message identity';
  ASSERT topic_size(TEST_TOPIC) = 2,
    'topic should still have size 2';

  RAISE INFO 'Tests all passed!';
END;
$$ LANGUAGE plpgsql;

ROLLBACK;

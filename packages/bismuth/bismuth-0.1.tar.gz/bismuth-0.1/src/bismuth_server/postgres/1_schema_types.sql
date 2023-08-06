-- Create types. This file must be formatted exactly one line per statement as ALTER TYPE cannot run in a multi-statement.
DO $$ BEGIN IF NOT EXISTS (SELECT * FROM pg_type WHERE typname = 'hash_type') THEN CREATE TYPE hash_type AS ENUM (); END IF; END $$;
ALTER TYPE hash_type ADD VALUE IF NOT EXISTS 'sha256';
ALTER TYPE hash_type ADD VALUE IF NOT EXISTS 'sha384';
ALTER TYPE hash_type ADD VALUE IF NOT EXISTS 'sha512';

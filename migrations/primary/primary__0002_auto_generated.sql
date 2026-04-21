-- upgrade

ALTER TABLE users ADD COLUMN locked_out BOOLEAN NOT NULL DEFAULT FALSE

-- rollback

ALTER TABLE users DROP COLUMN locked_out

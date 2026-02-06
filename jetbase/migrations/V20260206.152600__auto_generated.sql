-- upgrade

ALTER TABLE users ADD COLUMN verified INTEGER NOT NULL;

CREATE UNIQUE INDEX ix_users_email ON users (email);

-- rollback

ALTER TABLE users DROP COLUMN verified;

DROP INDEX ix_users_email ON users;

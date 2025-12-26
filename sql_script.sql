CREATE DATABASE store_db;

CREATE USER shop_user WITH PASSWORD '<your_password>';
ALTER ROLE shop_user SET client_encoding TO 'utf8';
ALTER ROLE shop_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE shop_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE store_db TO shop_user;

\c store_db
GRANT ALL ON SCHEMA public TO shop_user;

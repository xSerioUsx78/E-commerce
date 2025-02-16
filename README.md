# Databse

```bash
$ sudo su - postgres
$ psql

CREATE DATABASE ecommerce_base;
CREATE USER ecommerce WITH PASSWORD 'ecommerce';
ALTER ROLE ecommerce SET client_encoding TO 'utf8';
ALTER ROLE ecommerce SET default_transaction_isolation TO 'read committed';
ALTER ROLE ecommerce SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_base TO ecommerce;
\q

exit;
```

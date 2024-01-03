CREATE DATABASE scraper_db;
CREATE USER scraper WITH PASSWORD '${SCRAPER_PG_PASSWORD}';
GRANT ALL PRIVILEGES ON DATABASE scraper_db TO scraper;
GRANT ALL ON SCHEMA public TO scraper;
GRANT ALL ON SCHEMA public TO dbt_user;

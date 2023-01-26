#!/usr/bin/env bash
set -e

echo "$(date) ... started initializing database"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
create role tezaurs_public with nologin;

create table if not exists entries (
  entry_id serial primary key,
  entry varchar(100) not null,
  definition text not null,
  inserted_on timestamp not null
);

create table if not exists possible_neologisms (
  id serial primary key,
  possible_neologism text not null,
  count int not null default 1
);
EOSQL

echo "$(date) ... initialization finished, database is running"

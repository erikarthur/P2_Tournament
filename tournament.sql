-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--drop database if exists tournament;

--create database tournament;--

DROP TABLE if EXISTS players CASCADE;

CREATE TABLE players
(
  id serial NOT NULL,
  name text,
  CONSTRAINT key PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE players
  OWNER TO vagrant;
GRANT ALL ON TABLE players TO vagrant;
--GRANT SELECT, UPDATE, INSERT, TRUNCATE, DELETE ON TABLE players TO public;

DROP TABLE if EXISTS standings CASCADE;

CREATE TABLE standings
(
  id serial NOT NULL,
  player_id  INT NOT NULL,
  matches INT NOT NULL,
  wins  INT NOT NULL,
  losses INT NOT NULL,
  ties INT NOT NULL,
  used_bye boolean NOT NULL DEFAULT false
)
WITH (
  OIDS=FALSE
);
ALTER TABLE standings
  OWNER TO vagrant;
GRANT ALL ON TABLE standings TO vagrant;
--GRANT SELECT, UPDATE, INSERT, TRUNCATE, DELETE ON TABLE standings TO public;

CREATE OR REPLACE VIEW player_standings_view AS
 SELECT players.id,
    players.name,
    standings.wins,
    standings.matches
   FROM standings,
    players
  WHERE players.id = standings.id
  ORDER BY standings.wins DESC, players.name;

ALTER TABLE "player_standings_view"
  OWNER TO vagrant;

CREATE OR REPLACE VIEW swiss_pairings_view AS
 SELECT players.id,
    players.name,
    standings.wins,
    random() AS seed,
    standings.ties,
    standings.used_bye
   FROM standings,
    players
  WHERE players.id = standings.id
  ORDER BY standings.wins DESC, seed DESC;

ALTER TABLE swiss_pairings_view
  OWNER TO vagrant;

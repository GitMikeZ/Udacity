-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS rounds CASCADE;
DROP VIEW IF EXISTS standings CASCADE;

\c tournament

CREATE TABLE players(
    player_id serial PRIMARY KEY,
    player_name text
);

CREATE TABLE rounds(
    player_id serial PRIMARY KEY,
    winner integer references players(player_id),
    loser integer references players(player_id)
);

CREATE VIEW standings AS
SELECT players.player_id, players.player_name, FROM players
(SELECT count(*) FROM rounds WHERE rounds.winner = players.player_id) as gameWon,
(SELECT count(*) FROM rounds WHERE players.player_id in (winner, loser)) as gamePlayed
GROUP BY players.player_id
ORDER BY gameWon DESC;
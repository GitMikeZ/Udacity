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
SELECT p.player_id as player_id, p.player_name,
(SELECT count(*) FROM rounds WHERE rounds.winner = p.player_id) as won,
(SELECT count(*) FROM rounds WHERE p.player_id in (winner, loser)) as played
FROM players p
GROUP BY p.player_id
ORDER BY won DESC;
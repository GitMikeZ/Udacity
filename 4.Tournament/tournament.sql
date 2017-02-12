-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

CREATE TABLE players(
    id serial PRIMARY KEY,
    name text
);

CREATE TABLE rounds(
    id serial PRIMARY KEY,
    winner integer references players(id),
    loser integer references players(id)
);

CREATE VIEW standings AS
SELECT temp.id as id, temp.name,
(SELECT count(*) FROM rounds WHERE rounds.winner = temp.id) as won,
(SELECT count(*) FROM rounds where temp.id in (winner, loser)) as matches
FROM players temp
GROUP BY temp.id
ORDER BY won DESC;

# Tournament

A swiss tournament psql database schema used to store a game between players and test various coded functions.

## Funcionalities of tournament.py
connect()
    -Connects to PostgreSQL database and return connection

deleteMatches()
    -Remove all match records of the swiss game from the db

deletePlayers()
    -Remove all player records from the db

countPlayers()
    -Retruns the number of players within the swiss game

registerPlayers(name)
    -Registers a player

playerStanding
    -Returns a list of id, name, wins nad matches of all players sorted
     by wins

reportMatch
    -Records into the db the winner and loser of a single match

swissPairings()
    -Returns a list of id1, name1, id2, name2 of the swiss game

## Run

1. Install Vagrant and VirtualBox
2. Clone the full-stack-nanodegree-vm repository
3. Launch the Vagrant VM by opening git shell and cd into the vagrant folder
4. Type $vagrant up (powers the VM) and $vagrant ssh (logs into VM) to start
5. cd into the tournament directory: $cd /vagrant/tournament
6. Type $psql and run =>\i tournament.sql to connect to the db
7. \q to exit psql
8. Run the $python tournament_test.py to test the tournament.py

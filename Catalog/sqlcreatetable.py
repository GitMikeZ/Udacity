import sqlite3
conn = sqlite3.connect('teamwithplayer.db')

c = conn.cursor()
c.execute('''
          CREATE TABLE team
          (id INTEGER PRIMARY KEY ASC, name varchar(250) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE player_item
          (id INTEGER PRIMARY KEY ASC,
           name varchar(250),
           number varchar(250),
           description varchar(250) NOT NULL,
           team_id INTEGER NOT NULL,
           FOREIGN KEY(team_id) REFERENCES team(id))
          ''')

conn.commit()
conn.close()

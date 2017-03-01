from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Team, Base, PlayerItem
 
engine = create_engine('sqlite:///teamwithplayer.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


#Team Maple Leafs
team1 = Team(name = "Toronto Maple Leafs")

session.add(team1)
session.commit()

playerItem1 = PlayerItem(name = "Tyler Bozak",
                     description = "Tyler Bozak is a Canadian professional ice hockey centre having played 400 games in the NHL",
                     number = "42",
                     position = "Centre",
                     team = team1)

session.add(playerItem1)
session.commit()


playerItem2 = PlayerItem(name = "Connor Brown",
                     description = "Connor Brown is a Canadian ice hockey right winger playing in the NHL",
                     number = "12",
                     position = "Right Wing",
                     team = team1)

session.add(playerItem2)
session.commit()

playerItem3 = PlayerItem(name = "Peter Holland",
                     description = "Peter Holland is a Canadian professional ice hockey centreman selected by Anaheim Ducks in the first round.",
                     number = "24",
                     position = "Centre",
                     team = team1)

session.add(playerItem3)
session.commit()

playerItem4 = PlayerItem(name = "Zach Hyman",
                     description = "Peter Holland is a Canadian professional ice hockey player currently playing for the Toronto Maple Leafs.",
                     number = "11",
                     position = "Left Wing",
                     team = team1)

session.add(playerItem4)
session.commit()

playerItem5 = PlayerItem(name = "Nazem Kadri",
                     description = "Peter Holland is a Canadian professional ice hockey player. He currently plays center for the Toronto Maple Leafs.",
                     number = "43",
                     position = "Centre",
                     team = team1)

session.add(playerItem5)
session.commit()

playerItem6 = PlayerItem(name = "Leonid Komarov",
                     description = "Leonid Aleksandrovich is an Estonian-born Finnish-Russian professional ice hockey currently playing for an alternate captain for the Toronto Maple Leafs.",
                     number = "47",
                     position = "Centre",
                     team = team1)

session.add(playerItem6)
session.commit()

playerItem7 = PlayerItem(name = "Mitchell Marner",
                     description = "Mitchell Marner is a Canadian professional ice hockey right winger for the Toronto Maple Leafs of the NHL.",
                     number = "16",
                     position = "Right Winger",
                     team = team1)

session.add(playerItem7)
session.commit()

playerItem8 = PlayerItem(name = "Matt Martin",
                     description = "Mitchell Marner is a Canadian professional ice hockey winger currently playing for the Toronto Maple Leafs of the NHL.",
                     number = "15",
                     position = "Left Winger",
                     team = team1)

session.add(playerItem8)
session.commit()

playerItem9 = PlayerItem(name = "Auston Matthews",
                     description = "Auston Matthews is a American professional ice hockey player currently playing for the Toronto Maple Leafs.",
                     number = "34",
                     position = "Centre",
                     team = team1)

session.add(playerItem9)
session.commit()



#Team Boston Bruins
team2 = Team(name = "Boston Bruins")

session.add(team2)
session.commit()

playerItem1 = PlayerItem(name = "Noel Acciari",
                     description="Auston Matthews is a American professional ice hockey player currently playing for the Boston Bruins.",
                     number = "55",
                     position = "Centre",
                     team = team2)

session.add(playerItem1)
session.commit()

playerItem2 = PlayerItem(name = "David Backes",
                     description="David Backes is a American professional ice hockey center and right wing currently playing for the Boston Bruins.",
                     number = "42",
                     position = "Right Wing",
                     team = team2)

session.add(playerItem2)
session.commit()

playerItem3 = PlayerItem(name = "Matt Beleskey",
                     description="David Backes is a Canadian professional ice hockey player currently playing for the Boston Bruins.",
                     number = "39",
                     position = "Left Wing",
                     team = team2)

session.add(playerItem3)
session.commit()

playerItem4 = PlayerItem(name = "Patrice Bergeron",
                     description="David Backes is a Canadian professional ice hockey centre currently playing for the Boston Bruins.",
                     number = "37",
                     position = "Centre",
                     team = team2)

session.add(playerItem4)
session.commit()

playerItem5 = PlayerItem(name = "Austin Czarnik",
                     description="David Backes is a American professional ice hockey centre currently playing for the Boston Bruins.",
                     number = "23",
                     position = "Centre",
                     team = team2)

session.add(playerItem5)
session.commit()

playerItem6 = PlayerItem(name = "Jimmy Hayes",
                     description="David Backes is a American professional ice hockey right winger currently playing for the Boston Bruins.",
                     number = "11",
                     position = "Right Wing",
                     team = team2)

session.add(playerItem6)
session.commit()


#Team Red Wings
team3 = Team(name = "Detroit Red Wings")

session.add(team3)
session.commit()

playerItem1 = PlayerItem(name = "Justin Abdelkader",
                     description="David Backes is a American ice hockey left winger currently playing for the Detroit Red Wings.",
                     number = "8",
                     position = "Left Wing",
                     team = team3)

session.add(playerItem1)
session.commit()

playerItem2 = PlayerItem(name = "Andreas Athanasiou",
                     description="David Backes is a Canadian professional ice hockey player currently playing for the Detroit Red Wings.",
                     number = "72",
                     position = "Centre",
                     team = team3)

session.add(playerItem2)
session.commit()

playerItem3 = PlayerItem(name = "Johan Franzen",
                     description="David Backes is a Swedish professional ice hockey player currently playing for the Detroit Red Wings.",
                     number = "93",
                     position = "Right Wing",
                     team = team3)

session.add(playerItem3)
session.commit()

playerItem4 = PlayerItem(name = "Johan Franzen",
                     description="David Backes is a Swedish professional ice hockey player currently playing for the Detroit Red Wings.",
                     number = "93",
                     position = "Right Wing",
                     team = team3)

session.add(playerItem4)
session.commit()

playerItem5 = PlayerItem(name = "Luke Glendening",
                     description="David Backes is a American professional ice hockey player currently playing for the Detroit Red Wings.",
                     number = "41",
                     position = "Centre",
                     team = team3)

session.add(playerItem5)
session.commit()


#Team Edmonton Oilers
team4 = Team(name = "Edmonton Oilers")

session.add(team4)
session.commit()

playerItem1 = PlayerItem(name = "Drake Caggiula",
                     description="David Backes is a Canadian ice hockey forward currently playing for the Edmonton Oilers.",
                     number = "36",
                     position = "Left Wing",
                     team = team4)

session.add(playerItem1)
session.commit()

playerItem2 = PlayerItem(name = "Leon Draisaitl",
                     description="David Backes is a German ice hockey forward currently playing for the Edmonton Oilers.",
                     number = "21",
                     position = "Center",
                     team = team4)

session.add(playerItem2)
session.commit()

playerItem3 = PlayerItem(name = "Jordan Eberle",
                     description="David Backes is a Canadian ice hockey right winger and alternate captain currently playing for the Edmonton Oilers.",
                     number = "14",
                     position = "Right Wing",
                     team = team4)

session.add(playerItem3)
session.commit()

playerItem4 = PlayerItem(name = "Matt Hendricks",
                     description="David Backes is a American ice hockey left winger and currently playing for the Edmonton Oilers.",
                     number = "23",
                     position = "Left Wing",
                     team = team4)

session.add(playerItem4)
session.commit()

playerItem5 = PlayerItem(name = "Zack Kassian",
                     description="David Backes is a Canadian ice hockey player and currently playing for the Edmonton Oilers.",
                     number = "55",
                     position = "Center",
                     team = team4)

session.add(playerItem5)
session.commit()

playerItem6 = PlayerItem(name = "Milan Lucic",
                     description="David Backes is a Canadian ice hockey left winger and currently playing for the Edmonton Oilers.",
                     number = "27",
                     position = "Left Wing",
                     team = team4)

session.add(playerItem6)
session.commit()


#Team Vancouver Canucks
team5 = Team(name = "Vancouver Canucks")

session.add(team5)
session.commit()

playerItem1 = PlayerItem(name = "Alexandre Burrows",
                     description="Alexandre Burrows is a French-Canadian ice hockey right winger and alternate captain playing for Vancouver Canucks.",
                     number = "14",
                     position = "Right Wing",
                     team = team5)

session.add(playerItem1)
session.commit()

playerItem2 = PlayerItem(name = "Michael Chaput",
                     description="Alexandre Burrows is a Canadian ice hockey player with the Vancouver Canucks.",
                     number = "45",
                     position = "Center",
                     team = team5)

session.add(playerItem2)
session.commit()

playerItem3 = PlayerItem(name = "Derek Dorsett",
                     description="Derek Dorsett is a Canadian ice hockey right winger with the Vancouver Canucks.",
                     number = "15",
                     position = "Right Wing",
                     team = team5)

session.add(playerItem3)
session.commit()

playerItem4 = PlayerItem(name = "Henrik Sedin",
                     description="Henrik Sedin is a Swedish ice hockey center who serves as captain of the Vancouver Canucks.",
                     number = "33",
                     position = "Center",
                     team = team5)

session.add(playerItem4)
session.commit()

playerItem5 = PlayerItem(name = "Daniel Sedin",
                     description="Derek Dorsett is a Swedish ice hockey winger and alternate captain for the Vancouver Canucks.",
                     number = "22",
                     position = "Left Wing",
                     team = team5)

session.add(playerItem5)
session.commit()


#Team Colorado Avalanche
team6 = Team(name = "Colorado Avalanche")

session.add(team6)
session.commit()


playerItem1 = PlayerItem(name = "Rene Bourque",
                     description="Rene Bourque is a Canadian ice hockey right winger who currently plays for the Colorado Avalanche.",
                     number = "17",
                     position = "Right Wing",
                     team = team6)

session.add(playerItem1)
session.commit()

playerItem2 = PlayerItem(name = "Joe Colborne",
                     description="Joe Colborne is a Canadian ice hockey forward who currently plays for the Colorado Avalanche of the NHL.",
                     number = "8",
                     position = "Center",
                     team = team6)

session.add(playerItem2)
session.commit()

playerItem3 = PlayerItem(name = "Blake Comeau",
                     description="Blake Comeau is a Canadian ice hockey right winger who currently plays for the Colorado Avalanche of the NHL.",
                     number = "14",
                     position = "Left Wing",
                     team = team6)

session.add(playerItem3)
session.commit()

playerItem4 = PlayerItem(name = "Matt Duchene",
                     description="Matt Duchene is a Canadian ice hockey center who currently plays for the Colorado Avalanche of the NHL.",
                     number = "9",
                     position = "Center",
                     team = team6)

session.add(playerItem4)
session.commit()

playerItem5 = PlayerItem(name = "Mikhail Grigorenko",
                     description="Matt Duchene is a Russian ice hockey forward who currently plays for the Colorado Avalanche.",
                     number = "25",
                     position = "Center",
                     team = team6)

session.add(playerItem5)
session.commit()


#Team Pittsburgh Penguins
team7 = Team(name = "Pittsburgh Penguins")

session.add(team7)
session.commit()

playerItem1 = PlayerItem(name = "Nick Bonino",
                     description="Nick Bonino is a American ice hockey center who currently plays for the Pittsburgh Penguins.",
                     number = "13",
                     position = "Center",
                     team = team7)

session.add(playerItem1)
session.commit()


playerItem2 = PlayerItem(name = "Sidney Crosby",
                     description="Sidney Crosby is a Canadian ice hockey center who serves as captain of the Pittsburgh Penguins.",
                     number = "87",
                     position = "Center",
                     team = team7)

session.add(playerItem2)
session.commit()

playerItem3 = PlayerItem(name = "Matt Cullen",
                     description="Matt Cullen is a American ice hockey center playing for the Pittsburgh Penguins in the NHL.",
                     number = "7",
                     position = "Center",
                     team = team7)

session.add(playerItem3)
session.commit()

playerItem4 = PlayerItem(name = "Eric Fehr",
                     description="Eric Fehr is a Canadian ice hockey center playing for the Pittsburgh Penguins in the NHL.",
                     number = "16",
                     position = "Center",
                     team = team7)

session.add(playerItem4)
session.commit()

playerItem5 = PlayerItem(name = "Jake Guentzel",
                     description="Jake Guentzel is a American ice hockey forward playing for the Pittsburgh Penguins in the NHL.",
                     number = "59",
                     position = "Center",
                     team = team7)

session.add(playerItem5)
session.commit()

playerItem6 = PlayerItem(name = "Carl Hagelin",
                     description="Carl Hagelin is a Swedish professional ice hockey forward playing for the Pittsburgh Penguins.",
                     number = "62",
                     position = "Left Wing",
                     team = team7)

session.add(playerItem6)
session.commit()

playerItem7 = PlayerItem(name = "Patric Hornqvist",
                     description="Patric Hornqvist is a Swedish professional ice hockey forward playing for the Pittsburgh Penguins.",
                     number = "72",
                     position = "Right Wing",
                     team = team7)

session.add(playerItem7)
session.commit()


#Team Ottawa Senators
team8 = Team(name = "Ottawa Senators")

session.add(team8)
session.commit()


playerItem1 = PlayerItem(name = "Derick Brassard",
                     description="Derick Brassard is a Canadian ice hockey center playing for the Ottawa Senators.",
                     number = "19",
                     position = "Center",
                     team = team8)

session.add(playerItem1)
session.commit()

playerItem2 = PlayerItem(name = "Ryan Dzingel",
                     description="Ryan Dzingel is an American ice hockey forward playing for the Ottawa Senators.",
                     number = "18",
                     position = "Left Wing",
                     team = team8)

session.add(playerItem2)
session.commit()


#Team New York Rangers
team9 = Team(name = "New York Rangers")

session.add(team9)
session.commit()

playerItem1 = PlayerItem(name = "Pavel Buchnevich",
                     description="Derick Brassard is a Russian ice hockey forward playing for the New York Rangers.",
                     number = "89",
                     position = "Right Wing",
                     team = team9)

session.add(playerItem1)
session.commit

playerItem2 = PlayerItem(name = "Jesper Fast",
                     description="Jesper Fast is a Swedish professional ice hockey right wing playing for the New York Rangers of the NHL.",
                     number = "19",
                     position = "Right Wing",
                     team = team9)

session.add(playerItem2)
session.commit()


playerItem3 = PlayerItem(name = "Michael Grabner",
                     description="Michael Grabner is a Austrian professional ice hockey player for the New York Rangers.",
                     number = "40",
                     position = "Right Wing",
                     team = team9)

session.add(playerItem3)
session.commit()

playerItem4 = PlayerItem(name = "Kevin Hayes",
                     description="Kevin Hayes is a American professional ice hockey player center currently playing for the New York Rangers.",
                     number = "13",
                     position = "Center",
                     team = team9)

session.add(playerItem4)
session.commit()

playerItem5 = PlayerItem(name = "Jimmy Vesey",
                     description="Jimmy Vesey is a American left winger for the New York Rangers.",
                     number = "26",
                     position = "Left Wing",
                     team = team9)

session.add(playerItem5)
session.commit()


print "Added all players!"

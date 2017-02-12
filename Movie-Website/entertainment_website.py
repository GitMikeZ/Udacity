# Project: Movie Trailer Website
# Written by: iQnim
# Date: October 29, 2016

import fresh_tomatoes
import movie

#Create movie instance lotr1 and store instance variables into constructor  
lotr1 = movie.Movie("The Lord of the Rings: The Fellowship of the Ring",
                    "A meek Hobbit from the Shire and eight companions"
                    "set out on a journey to destroy the powerful One"
                    "Ring and save Middle Earth from the Dark Lord Sauron.",
                    "https://upload.wikimedia.org/wikipedia/en/9/9d/The_Lord_of_the_Rings_The_Fellowship_of_the_Ring_%282001%29_theatrical_poster.jpg", # NOQA
                    "https://www.youtube.com/watch?v=V75dMMIW2B4")

#Create movie instance lotr2 and store instance variables into constructor   
lotr2 = movie.Movie("The Lord of the Rings: The Two Towers",
                    "While Frodo and Sam edge closer to Mordor with"
                    "the help of the shifty Gollum, the divided fellowship"
                    "makes a stand against Sauron's new ally, Saruman,"
                    "and his hordes of Isengard.",
                    "https://upload.wikimedia.org/wikipedia/en/a/ad/Lord_of_the_Rings_-_The_Two_Towers.jpg", # NOQA
                    "https://www.youtube.com/watch?v=LbfMDwc4azU")

#Create movie instance lotr3 and store instance variables into constructor 
lotr3 = movie.Movie("The Lord of the Rings: The Return of the King",
                    "Gandalf and Aragorn lead the World of Men against"
                    "Sauron's army to draw his gaze from Frodo and Sam"
                    "as they approach Mount Doom with the One Ring.",
                    "https://upload.wikimedia.org/wikipedia/en/9/9d/Lord_of_the_Rings_-_The_Return_of_the_King.jpg", # NOQA
                    "https://www.youtube.com/watch?v=r5X-hFf6Bwo")

#Create movie instance sw1 and store instance variables into constructor 
sw1 = movie.Movie("Star Wars: Episode I – The Phantom Menace",
                  "Two Jedi Knights escape a hostile blockade to find"
                  "allies and come across a young boy who may bring"
                  "balance to the Force, but the long dormant Sith"
                  "resurface to reclaim their old glory.",
                  "https://upload.wikimedia.org/wikipedia/en/4/40/Star_Wars_Phantom_Menace_poster.jpg", # NOQA
                  "https://www.youtube.com/watch?v=bD7bpG-zDJQ")

#Create movie instance sw2 and store instance variables into constructor 
sw2 = movie.Movie("Star Wars: Episode II – Attack of the Clones",
                  "Ten years after initially meeting, Anakin Skywalker"
                  "shares a forbidden romance with Padmé, while Obi-Wan"
                  "investigates an assassination attempt on the Senator"
                  "and discovers a secret clone army crafted for the Jedi.",
                  "https://upload.wikimedia.org/wikipedia/en/3/32/Star_Wars_-_Episode_II_Attack_of_the_Clones_%28movie_poster%29.jpg", # NOQA
                  "https://www.youtube.com/watch?v=gYbW1F_c9eM")

#Create movie instance sw3 and store instance variables into constructor 
sw3 = movie.Movie("Star Wars: Episode III - Revenge of the Sith",
                  "During the near end of the clone wars, Darth"
                  "Sidious has revealed himself and is ready to"
                  "execute the last part of his plan to rule the Galaxy.",
                  "https://upload.wikimedia.org/wikipedia/en/9/93/Star_Wars_Episode_III_Revenge_of_the_Sith_poster.jpg", # NOQA
                  "https://www.youtube.com/watch?v=5UnjrG_N8hU")


#Create movieArr array to store all the movie instance 
movieArr = [sw1, sw2, sw3, lotr1, lotr2, lotr3]

#Call fresh_tomatoes' instance method open_movies_page passing in movieArr
fresh_tomatoes.open_movies_page(movieArr)

# Project: Movie Trailer Website
# Written by: iQnim
# Date: October 29, 2016

import webbrowser

class Movie():

    #Constructor of Movie class
    def __init__(self, movie_title, movie_storyline,
                 poster_image, trailer_youtube):
        #Assign Instance Variables
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    #Show_trailer Instance Method
    def show_trailer(self):
        #Open the youtube link in the browser
        webbrowser.open(self.trailer_youtube_url)
        

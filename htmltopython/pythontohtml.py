#Project: Interview Practice (Full Stack)
#Written by: iQnim
#Date: February 3rd, 2017

import webapp2

#List of fruits and vegetables as Strings
my_list = ['Apples', 'Carrots', 'Oranges', 'Cabbage', 'Kiwi']

#HTML String
HTML_String = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Python to HTML</title>
</head>
<body>
'''

#for loop to add each list item to HTML unordered list
for items in my_list:
    HTML_String += '<ul>%s</ul>\n' % items

HTML_String += '</body>'

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(HTML_String)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

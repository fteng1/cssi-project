import webapp2
import jinja2
import os

from google.appengine.ext import ndb

class User(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    dates = ndb.JsonProperty(required=True)


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/log_in.html')
<<<<<<< HEAD
        self.response.write("This is the beginning of our project.")
=======
        self.response.write(welcome_template.render())
>>>>>>> 2ca6d09b169d74d5762972c630e3eeb9898102e6



#https://www.dw.com/image/48688022_303.jpg
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

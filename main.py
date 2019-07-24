import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users


class User(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    dates = ndb.JsonProperty(required=True)


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

user = users.get_current_user()

class MainPage(webapp2.RequestHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/log_in.html')
        self.response.write("This is the beginning of our project.")
        self.response.write(welcome_template.render())

class infoPage(webapp2.RequestHandler):
    def get(self):
        info_template = JINJA_ENVIRONMENT.get_template('templates/info_page.html')
        self.response.write(info_template.render())

class CalendarPage(webapp2.RequestHandler):
    def get(self):
        calendar_template = JINJA_ENVIRONMENT.get_template('templates/calendar.html')
        self.response.write(calendar_template.render())


#https://www.dw.com/image/48688022_303.jpg
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users

class ModelWithUser(ndb.Model):
    user_id = ndb.StringProperty()
    color = ndb.StringProperty()

    @classmethod
    def get_by_user(cls, user):
        return cls.query().filter(cls.user_id == user.user_id()).get()

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
        welcome_template = JINJA_ENVIRONMENT.get_template('log_in.html')
        self.response.write("This is the beginning of our project.")
        self.response.write(welcome_template.render())

        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                nickname, logout_url)
        else:
            login_url = users.create_login_url('/') #replace / with whatever url you want
            greeting = '<a href="{}">Sign in</a>'.format(login_url)
        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))
        #print(user.user_id)
#https://www.dw.com/image/48688022_303.jpg
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

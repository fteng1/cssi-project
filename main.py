import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users
from models import ModelWithUser



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        main_template = JINJA_ENVIRONMENT.get_template('log_in.html')
        self.response.write(main_template.render())
        #the code for the sign-in and -out button
        user = users.get_current_user()
        my_users = ModelWithUser.query().filter(ModelWithUser.user_id == user.user_id()).fetch(1)

        if len(my_users) == 1:
            current_user = my_users[0]
        else:
            current_user = ModelWithUser(user_id=user.user_id(), nickname=user.nickname())
            current_user.put()

        if user:
            logout_url = users.create_logout_url('/')
            if current_user is None:
                greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                    current_user.nickname, logout_url)
            else:
                greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                    current_user.first_name, logout_url)
        else:
            login_url = users.create_login_url('/welcome') #replace / with whatever url you want
            greeting = '<a href="{}">Sign in</a>'.format(login_url)
        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('welcome_back.html')
        username = users.get_current_user()
        self.response.write(welcome_template.render())

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        welcome_template = JINJA_ENVIRONMENT.get_template('welcome_back.html')
        welcome_dict = {
            "username": username,
        }
        self.response.write(welcome_template.render(welcome_dict))
    def post(self):
        user = users.get_current_user()
        my_nickname = self.request.get('Nickname')
        my_profile = Profile(nickname=my_nickname,user_id=user.user_id())
        my_profile.nickname = my_nickname
        my_profile.user_id = my_user.my_user_id()
        my_profile.put()
        username = my_nickname
        welcome_template = JINJA_ENVIRONMENT.get_template('welcome_back.html')
        username = my_nickname
        welcome_dict = {
            "username": username,
        }

#https://www.dw.com/image/48688022_303.jpg
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/welcome', WelcomePage),
    ('/profile', ProfilePage),
    ('/info', Infopage),
], debug=True)

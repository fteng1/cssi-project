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
        if ModelWithUser.query().filter(ModelWithUser.user_id == user.user_id()).fetch(1) is not None:
            current_user = check_profile_exists(ModelWithUser())
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

def welcome_dict(nameValue):
    welcome_dict = {
        "username": nameValue,
    }
    return welcome_dict

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('welcome_back.html')
        username = users.get_current_user()
        self.response.write(welcome_template.render())
    def post(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('welcome_back.html')
        nickname = self.request.get('Nickname')
        self.response.write(welcome_template.render(welcome_dict(nickname)))
        #update the nickname in the datastore
        user_profile(self,0,'Nickname',nickname)

def check_profile_exists(value):
    user = users.get_current_user()
    my_profiles = ModelWithUser.query().filter(ModelWithUser.user_id == user.user_id()).fetch()
    if len(my_profiles) == 1:
        my_profile = my_profiles[0]
    else:
        my_profile = value #will either be None of the Profile creator class
        #my_profile = Profile()
    return my_profile

def user_profile(self,create_new_user,update_source,updated_value):
    if create_new_user == 1:
         check_profile_exists(ModelWithUser())
         # self.response.write(welcome_template.render(welcome_dict(user)))
    else:
        user = users.get_current_user()
        updated_value = self.request.get(update_source)
        my_profile = check_profile_exists(ModelWithUser(nickname=updated_value,first_name=updated_value,user_id=user.user_id()))
        my_profile.nickname = updated_value
        my_profile.user_id = user.user_id()
        my_profile.put()

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        welcome_template = JINJA_ENVIRONMENT.get_template('welcome_back.html')
        self.response.write(welcome_template.render(welcome_dict(user)))
    def post(self):
        user = users.get_current_user()
        my_nickname = self.request.get('Nickname')
        my_profile = ModelWithUser(nickname=my_nickname,user_id=user.user_id())
        my_profile.nickname = my_nickname
        my_profile.user_id = user.user_id()
        my_profile.put()
        welcome_template = JINJA_ENVIRONMENT.get_template('welcome_back.html')
        welcome_dict(my_nickname)

#https://www.dw.com/image/48688022_303.jpg
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/welcome', WelcomePage),
    ('/profile', ProfilePage),
], debug=True)

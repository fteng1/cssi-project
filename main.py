import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users
from models import ModelWithUser
from datetime import datetime
from datetime import timedelta


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
        self.response.write(welcome_template.render(welcome_dict(my_nickname)))
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
        welcome_dict(username)

class CalendarPage(webapp2.RequestHandler):
    def get(self):
        calendar_template = JINJA_ENVIRONMENT.get_template('calendar.html')
        user = users.get_current_user()
        self.response.write(calendar_template.render())

    def post(self):
        calendar_template = JINJA_ENVIRONMENT.get_template('calendar_success.html')
        user = users.get_current_user()
        start_string = self.request.get('starttime')
        start_date = datetime.strptime(start_string, "%Y-%m-%dT%H:%M")
        start_utc = start_date + timedelta(hours=7)
        end_utc = start_utc + timedelta(hours=1)
        calendar_url = "http://www.google.com/calendar/event?action=TEMPLATE&text=%s&dates=%s/%s"
        calendar_start = start_utc.strftime("%Y%m%dT%H%M00Z")
        calendar_end = end_utc.strftime("%Y%m%dT%H%M00Z")
        event_type = self.request.get("event-type")
        if event_type == "birth-control":
            event_type_formatted = "Birth Control Medication"
        elif event_type == "doctor-appointment":
            event_type_formatted = "Doctor's Appointment"
        elif event_type == "other":
            event_type_formatted = "Other"
        else:
            event_type_formatted = "Pick Up Prescription"
        calendar_link = calendar_url % (event_type_formatted, calendar_start, calendar_end)
        calendar_dict = {
            "calendar_link": calendar_link,
        }
        self.response.write(calendar_template.render(calendar_dict))

class Infopage(webapp2.RequestHandler):
    def get(self):
        info_template = JINJA_ENVIRONMENT.get_template('info.html')
        user = users.get_current_user()
        self.response.write(info_template.render())

#https://www.dw.com/image/48688022_303.jpg
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/welcome', WelcomePage),
    ('/profile', ProfilePage),
    ('/info', Infopage),
    ('/calendar', CalendarPage),
], debug=True)

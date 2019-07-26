import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from google.appengine.api import users
from models import ModelWithUser
from models import Event
from datetime import datetime
from datetime import timedelta


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        #the code for the sign-in and -out button
        user = users.get_current_user()
        #if ModelWithUser.query().filter(ModelWithUser.user_id == user.user_id()).fetch(1) is not None:
        current_user = check_profile_exists(ModelWithUser())
        current_user.put()
        if user:
            logout_url = users.create_logout_url('/')
            if current_user is None:
                greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                    current_user.first_name, logout_url)
            else:
                greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                    current_user.nickname, logout_url)
        else:
            login_url = users.create_login_url('/welcome') #replace / with whatever url you want
            greeting = '<a href="{}">Sign in</a>'.format(login_url)
        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))
        main_template = JINJA_ENVIRONMENT.get_template('log_in.html')
        self.response.write(main_template.render())

def welcome_dict(nameValue):
    welcome_dict = {
        "username": nameValue,
    }
    return welcome_dict

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('welcome_back.html')
        user = users.get_current_user()
        username = user.nickname
        self.response.write(welcome_template.render(welcome_dict(username)))
    def post(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('welcome_back.html')
        user = users.get_current_user()
        username = user.nickname
        self.response.write(welcome_template.render(welcome_dict(username)))
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
        my_profile.user_id = user.user_id()
        my_profile.put()
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
        my_profile = check_profile_exists(ModelWithUser())
        profile_template = JINJA_ENVIRONMENT.get_template('profile.html')
        profile_pic = my_profile.profile_pic
        my_nickname = my_profile.nickname
        profile_dict = {
            "image_source": profile_pic,
            "nickname": my_nickname,
            "user_id": my_profile.user_id,
            #"Date Joined": "2019",
            #"Last Updated": "2019",
        }
        self.response.write(profile_template.render(profile_dict))

    def post(self):
        user = users.get_current_user()
        my_profile = check_profile_exists(ModelWithUser())
        my_profile = ModelWithUser.query().filter(ModelWithUser.user_id == user.user_id()).fetch()
        my_profile = my_profile[0]
        if self.request.get('Nickname') == "":
            my_nickname = my_profile.nickname
        else:
            my_nickname = self.request.get('Nickname')
            user_profile(self,0,'Nickname',my_nickname)

        if self.request.get('image_source') == "":
            profile_pic = my_profile.profile_pic
        else:
            profile_pic = self.request.get('image_source')
            my_profile.profile_pic = profile_pic
            my_profile.user_id = user.user_id()
            my_profile.put()

        profile_dict = {
            "image_source": profile_pic,
            "nickname": my_nickname,
            "user": user,
        }
        #update the nickname in the datastore

        profile_template = JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(profile_template.render(profile_dict))

class CalendarPage(webapp2.RequestHandler):
    def get(self):
        calendar_template = JINJA_ENVIRONMENT.get_template('calendar.html')
        user = users.get_current_user()

        # renders user's current existing events
        event_list = Event.query().filter(Event.owner == user.user_id()).order(Event.start).fetch()
        event_dict = {
            "event_list": event_list
        }
        self.response.write(calendar_template.render(event_dict))

    def post(self):
        user = users.get_current_user()

        if self.request.get("action") == "Add to Calendar":
            calendar_template = JINJA_ENVIRONMENT.get_template('calendar_success.html')
            # parses the inputted time and event type
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

            # generates the Google Calendar link, stores the event in the database and renders the page
            calendar_link = calendar_url % (event_type_formatted, calendar_start, calendar_end)
            event = Event(start=start_date, end=start_date + timedelta(hours=1), type=event_type_formatted, owner=user.user_id(), google_calendar=calendar_link)
            event.put()
            calendar_dict = {
                "calendar_link": calendar_link,
            }
            self.response.write(calendar_template.render(calendar_dict))
        else:
            key = self.request.get("event-id")
            event_list = Event.query().filter(Event.owner == user.user_id()).fetch()
            for event in event_list:
                if str(event.key) == key:
                    selected_event = event
            selected_event.key.delete()
            self.get()

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

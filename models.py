from google.appengine.ext import ndb

class ModelWithUser(ndb.Model):
    nickname = ndb.StringProperty(required=True)
    user_id = ndb.StringProperty()
    joined_on = ndb.DateTimeProperty(auto_now_add=True) #changes when it is first created
    updated_on = ndb.DateTimeProperty(auto_now=True) #changes whenever its active

    @classmethod
    def get_by_user(cls, user):
        return cls.query().filter(cls.user_id == user.user_id()).get()

from google.appengine.ext import ndb

class ModelWithUser(ndb.Model):
    user_id = ndb.StringProperty()
    color = ndb.StringProperty()

    @classmethod
    def get_by_user(cls, user):
        return cls.query().filter(cls.user_id == user.user_id()).get()

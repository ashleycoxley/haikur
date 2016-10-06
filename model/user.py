from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    password_hash = ndb.StringProperty(required=True)
    join_date = ndb.DateTimeProperty(auto_now_add=True)

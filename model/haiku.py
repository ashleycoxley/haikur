from google.appengine.ext import ndb
from user import User

class Haiku(ndb.Model):
    user_key = ndb.KeyProperty(kind=User)
    username = ndb.StringProperty(required=True)
    stanza1 = ndb.StringProperty(required=True)
    stanza2 = ndb.StringProperty(required=True)
    stanza3 = ndb.StringProperty(required=True)
    color = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    edited_date = ndb.DateTimeProperty()
    upvotes = ndb.IntegerProperty(default=0)
    downvotes = ndb.IntegerProperty(default=0)
    upvote_usernames = ndb.StringProperty(repeated=True)
    downvote_usernames = ndb.StringProperty(repeated=True)

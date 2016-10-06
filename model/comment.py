from google.appengine.ext import ndb
from haiku import Haiku
from user import User

class Comment(ndb.Model):
    haiku_ref = ndb.KeyProperty(kind=Haiku)
    user_key = ndb.KeyProperty(kind=User)
    username = ndb.TextProperty(required=True)
    comment_text = ndb.TextProperty(required=True)
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    edited_date = ndb.DateTimeProperty()

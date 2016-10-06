from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    password_hash = ndb.StringProperty(required=True)
    join_date = ndb.DateTimeProperty(auto_now_add=True)


class Haiku(ndb.Model):
    user_key = ndb.KeyProperty(kind=User)
    username = ndb.StringProperty(required=True)
    stanza1 = ndb.StringProperty(required=True)
    stanza2 = ndb.StringProperty(required=True)
    stanza3 = ndb.StringProperty(required=True)
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    edited_date = ndb.DateTimeProperty()
    upvotes = ndb.IntegerProperty(default=0)
    downvotes = ndb.IntegerProperty(default=0)


class Comment(ndb.Model):
    haiku_ref = ndb.KeyProperty(kind=Haiku)
    user_key = ndb.KeyProperty(kind=User)
    username = ndb.TextProperty(required=True)
    comment_text = ndb.TextProperty(required=True)
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    edited_date = ndb.DateTimeProperty()
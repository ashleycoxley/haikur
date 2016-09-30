import webapp2
import jinja2
import os
import re
import random
import string
import hashlib
import hmac

from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), 
    autoescape=True)

# DATASTORE 

class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    password_hash = ndb.StringProperty(required=True)
    join_date = ndb.DateTimeProperty(auto_now_add=True)


class Haiku(ndb.Model):
    content = ndb.TextProperty(required=True)
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    edited_date = ndb.DateTimeProperty()
    like_count = ndb.IntegerProperty(default=0)

    @classmethod
    def query_user(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)


class Comment(ndb.Model):
    username = ndb.StringProperty(required=True)
    comment = ndb.TextProperty(required=True)

    @classmethod
    def query_haiku(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)



# PAGE HANDLERS

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        haikus = Haiku.query().order(-Haiku.created_date)
        haiku_page = jinja_env.get_template('haiku.html')
        self.response.write(haiku_page.render(haikus=haikus))


class NewEntryHandler(webapp2.RequestHandler):
    def get(self):
        entry_form = jinja_env.get_template('newentry.html')
        self.response.write(entry_form.render())


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/newpost', NewEntryHandler)])

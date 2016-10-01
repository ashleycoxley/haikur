import webapp2
import jinja2
import os
import re
import random
import string
import hashlib
import hmac
import logging

from google.appengine.ext import ndb

logging.basicConfig(level=logging.INFO)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), 
    autoescape=True)


# VARIABLES

USER_RE = r"^[a-zA-Z0-9_-]{3,20}$"
PW_RE = r"^.{3,20}$"
EMAIL_RE = r"^[\S]+@[\S]+.[\S]+$"

INVALID_USERNAME_ERROR = "Invalid username"
USER_EXISTS_ERROR = "User already exists"
INVALID_PW_ERROR = "Invalid password"
PW_VERIFY_ERROR = "Passwords don't match"
INVALID_EMAIL_ERROR = "Invalid email address"

UNRECOGNIZED_USERNAME_ERROR = "That's not a valid user"
INCORRECT_PASSWORD_ERROR = "Incorrect password"

INCOMPLETE_STANZA_ERROR = "Fill out this stanza too!"
SYLLABLE_ERROR = "Are you sure that's %s syllables?"

SECRET = 'maple'

VALIDATION_RE = {
    'username': re.compile(USER_RE),
    'password': re.compile(PW_RE),
    'email': re.compile(EMAIL_RE)
    }

SIGNUP_ERROR_MESSAGES = {
    'username': INVALID_USERNAME_ERROR,
    'user_exists': USER_EXISTS_ERROR,
    'password': INVALID_PW_ERROR,
    'verify': PW_VERIFY_ERROR,
    'email': INVALID_EMAIL_ERROR
    }

LOGIN_ERROR_MESSAGES = {
    'username': UNRECOGNIZED_USERNAME_ERROR,
    'password': INCORRECT_PASSWORD_ERROR
    }

HAIKU_ERROR_MESSAGES = {
    'incomplete': INCOMPLETE_STANZA_ERROR,
    'syllables': SYLLABLE_ERROR
    }

# DATASTORE 

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
    like_count = ndb.IntegerProperty(default=0)


class Comment(ndb.Model):
    refers_to = ndb.KeyProperty(kind=Haiku)
    username = ndb.KeyProperty(kind=User)
    comment = ndb.TextProperty(required=True)



# HAIKU VALIDATION

def validate_haiku(haiku_list):
    template_values = {
        'stanza1': '',
        'stanza2': '',
        'stanza3': ''
        }

    form_valid = False
    template_values['stanza1_error'] = stanza_invalid(haiku_list[0], 5)
    template_values['stanza2_error'] = stanza_invalid(haiku_list[1], 7)
    template_values['stanza3_error'] = stanza_invalid(haiku_list[2], 5)

    if template_values['stanza1_error'] == "":
        template_values['stanza1'] = haiku_list[0]
    if template_values['stanza2_error'] == "":
        template_values['stanza2'] = haiku_list[1]
    if template_values['stanza3_error'] == "":
        template_values['stanza3'] = haiku_list[2]

    if template_values['stanza1_error'] == "" and template_values['stanza2_error'] == "" and template_values['stanza3_error'] == "":
        form_valid = True

    return form_valid, template_values


def stanza_invalid(stanza, syllable_count):
    # This will return '' if valid, and an error string if invalid:
    # HAIKU_ERROR['incomplete'] if it's empty
    # HAIKU_ERROR['syllables'] if syllables are 'wrong'
    if not stanza:
        return HAIKU_ERROR_MESSAGES['incomplete']
    else:
        return ""



# USER VALIDATION AND SIGNUP

def validate_signup_item(form_input, input_type):
    validation = VALIDATION_RE[input_type]
    return validation.match(form_input)


def user_exists(username):
    user_query = User.query(User.username==username)
    return user_query.get()


def validate_signup_form(username, password, verify, email):
    username_valid = validate_signup_item(username, 'username')
    password_valid = validate_signup_item(password, 'password')
    verify_valid = password == verify
    if email:
        email_valid = validate_signup_item(email, 'email')
    
    template_values = {
        'username': '',
        'email': '',
        'username_error': '',
        'password_error': '',
        'verify_error': '',
        'email_error': ''
        }

    form_valid = True
    if not username_valid:
        template_values['username_error'] = SIGNUP_ERROR_MESSAGES['username']
        form_valid = False
    else:
        if user_exists(username):
            template_values['username_error'] = SIGNUP_ERROR_MESSAGES['user_exists']
            form_valid = False
        else:
            template_values['username'] = username
    if not password_valid:
        template_values['password_error'] = SIGNUP_ERROR_MESSAGES['password']
        form_valid = False
    if not verify_valid:
        template_values['verify_error'] = SIGNUP_ERROR_MESSAGES['verify']
        form_valid = False
    if email and not email_valid:
        template_values['email_error'] = SIGNUP_ERROR_MESSAGES['email']
        form_valid = False
    else:
        template_values['email'] = email

    return form_valid, template_values


def login_valid(username, password):    
    template_values = {
        'username': '',
        'username_error': '',
        'password_error': ''
        }

    form_valid = True
    if user_exists(username) is None:
        template_values['username_error'] = LOGIN_ERROR_MESSAGES['username']
        form_valid = False
    else:
        if not login_password_valid(username, password):
            template_values['password_error'] = LOGIN_ERROR_MESSAGES['password']
            template_values['username'] = username
            form_valid = False

    return form_valid, template_values


def add_user(username, password, email):
    password_hash = hash_password(username, password)
    user = User(username=username, password_hash=password_hash)
    if email:
        user.email = email
    return user.put()



# ENCRYPTION AND COOKIES

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def hash_password(username, password, salt=None):
    if salt == None:
        salt = make_salt()
    h = hashlib.sha256(username + password + salt).hexdigest()
    return '%s,%s' % (h, salt)


def lookup_password(username):
    user_obj = User.query(User.username==username).get()
    return user_obj.password_hash


def validate_password(username, password, stored_password):
    salt = stored_password.split(',')[1]
    if hash_password(username, password, salt) == stored_password:
        return True
    else:
        return False


def login_password_valid(username, password):
    password_hash = lookup_password(username)
    return validate_password(username, password, password_hash)


def hash_cookie(user_id):
    user_hash = hmac.new(SECRET, user_id).hexdigest()
    return "%s|%s" % (user_id, user_hash)


def build_cookie_str(user_id):
    cookie_hash = hash_cookie(user_id)
    return 'user_id=%s; Path=/' % cookie_hash


def validate_cookie(cookie_hash):
    returned_user_id = cookie_hash.split('|')[0]
    if cookie_hash == hash_cookie(returned_user_id):
        return returned_user_id


# PAGE HANDLERS

class HaikurHandler(webapp2.RequestHandler):
    def set_user_cookie(self, user_id):
        user_id_str = str(user_id)
        cookie_str = build_cookie_str(user_id_str)
        self.response.headers.add_header('Set-Cookie', cookie_str)

    def read_user_cookie(self):
        cookie_hash = self.request.cookies.get('user_id')
        user_id = validate_cookie(cookie_hash)
        return user_id

    def remove_user_cookie(self):
        self.response.headers.add_header(
            'Set-Cookie',
            'user_id=; Path=/')

    def get_username_by_cookie(self):
        user_id = self.read_user_cookie()
        if user_id:
            user = User.get_by_id(int(user_id))
            return user.username


class MainPageHandler(HaikurHandler):
    def get(self):
        haikus = Haiku.query().order(-Haiku.created_date)
        signedin_username = self.get_username_by_cookie()
        if not signedin_username:
            signedin_username = ""
        haiku_page = jinja_env.get_template('haiku.html')
        self.response.write(haiku_page.render(
            haikus=haikus,
            signedin_username=signedin_username))


class NewEntryHandler(HaikurHandler):
    def get(self):
        signedin_username = self.get_username_by_cookie()
        if signedin_username:
            entry_form = jinja_env.get_template('newentry.html')
            self.response.write(entry_form.render(
                signedin_username=signedin_username))
        else:
            self.redirect('/login')

    def post(self):
        user_id = self.read_user_cookie()
        if not user_id:
            self.redirect('/login')

        stanza1 = self.request.get('stanza1')
        stanza2 = self.request.get('stanza2')
        stanza3 = self.request.get('stanza3')

        form_valid, template_values = validate_haiku([
            stanza1,
            stanza2,
            stanza3
            ])

        if form_valid:
            haiku = Haiku(
                user_key=User.get_by_id(int(user_id)).key,
                username=User.get_by_id(int(user_id)).username,
                stanza1=stanza1,
                stanza2=stanza2,
                stanza3=stanza3,
                )
            haiku_key = haiku.put()
            haiku_id = str(haiku_key.id())

            self.redirect('/' + haiku_id)

        else:
            entry_form = jinja_env.get_template('newentry.html')
            self.response.write(entry_form.render(
                stanza1=template_values['stanza1'],
                stanza2=template_values['stanza2'],
                stanza3=template_values['stanza3'],
                stanza1_error=template_values['stanza1_error'],
                stanza2_error=template_values['stanza2_error'],
                stanza3_error=template_values['stanza3_error']))


class SingleHaikuHandler(HaikurHandler):
    def get(self, haiku_id):
        haiku_key = ndb.Key('Haiku', int(haiku_id))
        haiku = haiku_key.get()

        if not haiku:
            self.error(404)
            return

        single_haiku_page = jinja_env.get_template('permalink.html')
        self.response.write(single_haiku_page.render(haiku=haiku))


class SignupHandler(HaikurHandler):
    def get(self):
        signup_form = jinja_env.get_template('/signup.html')
        self.response.write(signup_form.render())

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        form_valid, template_values = validate_signup_form(
            username,
            password,
            verify,
            email)

        if form_valid:
            user_key = add_user(username, password, email)
            if user_key:
                user_id = user_key.id()
                self.set_user_cookie(user_id)
                self.redirect('/')
            else:
                self.redirect('/signup')

        else:
            signup_form = jinja_env.get_template('/signup.html')
            self.response.write(signup_form.render(
                username=template_values['username'],
                email=template_values['email'],
                username_error=template_values['username_error'],
                password_error=template_values['password_error'],
                verify_error=template_values['verify_error'],
                email_error=template_values['email_error']))


class LoginHandler(HaikurHandler):
    def get(self):
        user_id = self.read_user_cookie()
        if user_id:
            self.redirect('/')
        else:
            login_page = jinja_env.get_template('login.html')
            self.response.write(login_page.render())

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        form_valid, template_values = login_valid(username, password)

        if form_valid:
            user_id = User.query(User.username==username).get().key.id()
            self.set_user_cookie(user_id)
            self.redirect('/')
        else:
            login_page = jinja_env.get_template('login.html')
            self.response.write(login_page.render(
                username=template_values['username'],
                username_error=template_values['username_error'],
                password_error=template_values['password_error'])
                )


class LogoutHandler(HaikurHandler):
    def get(self):
        self.remove_user_cookie()
        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/newpost', NewEntryHandler),
    ('/signup', SignupHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/(\w+)', SingleHaikuHandler)
    ])

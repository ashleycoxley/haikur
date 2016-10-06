import model
from global_vars import *
import re
import hmac
import random
import string
import hashlib


def validate_signup_item(form_input, input_type):
    validation = VALIDATION_RE[input_type]
    return validation.match(form_input)


def user_exists(username):
    user_query = model.User.query(model.User.username==username)
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


def add_user(username, password, email):
    password_hash = hash_password(username, password)
    user = model.User(username=username, password_hash=password_hash)
    if email:
        user.email = email
    return user.put()

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def hash_password(username, password, salt=None):
    if salt == None:
        salt = make_salt()
    h = hashlib.sha256(username + password + salt).hexdigest()
    return '%s,%s' % (h, salt)


def lookup_password(username):
    user_obj = model.User.query(model.User.username==username).get()
    return user_obj.password_hash


def validate_password(username, password, stored_password):
    salt = stored_password.split(',')[1]
    if hash_password(username, password, salt) == stored_password:
        return True
    else:
        return False


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

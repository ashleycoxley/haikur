import model
from global_vars import *
import re
import hmac
import random
import string
import hashlib


def user_exists(username):
    user_query = model.User.query(model.User.username==username)
    return user_query.get()


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

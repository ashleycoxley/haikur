import re
import os
import jinja2

TEMPLATE_DIR = os.path.join('templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR), 
    autoescape=True)

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

DEFAULT_COLOR = 'red'

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

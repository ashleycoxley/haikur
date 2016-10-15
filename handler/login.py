from handler_helper import HaikurHandler
import model
from helper.global_vars import *
from helper.user_validation import *


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


def login_password_valid(username, password):
    password_hash = lookup_password(username)
    return validate_password(username, password, password_hash)


class LoginHandler(HaikurHandler):
    def get(self):
        user_id = self.read_user_cookie()
        if user_id:
            self.redirect('/')
        else:
            login_page = JINJA_ENV.get_template('login.html')
            self.response.write(login_page.render())

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        form_valid, template_values = login_valid(username, password)

        if form_valid:
            user_id = model.User.query(model.User.username==username).get().key.id()
            self.set_user_cookie(user_id)
            self.redirect('/')
        else:
            login_page = JINJA_ENV.get_template('login.html')
            self.response.write(login_page.render(
                username=template_values['username'],
                username_error=template_values['username_error'],
                password_error=template_values['password_error'])
                )

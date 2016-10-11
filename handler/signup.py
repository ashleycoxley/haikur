from handler_helper import HaikurHandler
from helper.global_vars import *
import helper.user_validation
import model


def validate_signup_item(form_input, input_type):
    validation = VALIDATION_RE[input_type]
    return validation.match(form_input)


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
        if helper.user_validation.user_exists(username):
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
    password_hash = helper.user_validation.hash_password(username, password)
    user = model.User(username=username, password_hash=password_hash)
    if email:
        user.email = email
    return user.put()


class SignupHandler(HaikurHandler):
    def get(self):
        signup_form = JINJA_ENV.get_template('/signup.html')
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
            signup_form = JINJA_ENV.get_template('/signup.html')
            self.response.write(signup_form.render(
                username=template_values['username'],
                email=template_values['email'],
                username_error=template_values['username_error'],
                password_error=template_values['password_error'],
                verify_error=template_values['verify_error'],
                email_error=template_values['email_error']))

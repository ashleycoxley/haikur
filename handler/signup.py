from handler_helper import HaikurHandler
from helper.global_vars import JINJA_ENV


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
import webapp2
from helper import user_validation
from helper.global_vars import JINJA_ENV
import model

class HaikurHandler(webapp2.RequestHandler):
    def set_user_cookie(self, user_id):
        user_id_str = str(user_id)
        cookie_str = user_validation.build_cookie_str(user_id_str)
        self.response.headers.add_header('Set-Cookie', cookie_str)

    def read_user_cookie(self):
        cookie_hash = self.request.cookies.get('user_id')
        if cookie_hash:
            user_id = user_validation.validate_cookie(cookie_hash)
            return user_id

    def remove_user_cookie(self):
        self.response.headers.add_header(
            'Set-Cookie',
            'user_id=; Path=/')

    def get_username_by_cookie(self):
        user_id = self.read_user_cookie()
        if user_id:
            user = model.User.get_by_id(int(user_id))
            if user:
                return user.username

    def not_signed_in(self, user_id):
        print user_id
        if user_id is None:
            return True
        else:
            return False

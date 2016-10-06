from handler_helper import HaikurHandler

class LogoutHandler(HaikurHandler):
    def get(self):
        self.remove_user_cookie()
        self.redirect('/')
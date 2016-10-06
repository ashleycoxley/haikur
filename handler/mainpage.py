from handler_helper import HaikurHandler
import model
from helper.user_validation import *
from helper.global_vars import TEMPLATE_DIR, JINJA_ENV


class MainPageHandler(HaikurHandler):
    def get(self):
        haikus = model.Haiku.query().order(-model.Haiku.created_date)
        signedin_username = self.get_username_by_cookie()
        if signedin_username is None:
            signedin_username = ""
        haiku_page = JINJA_ENV.get_template('/haiku.html')
        for haiku in haikus:
            comments = model.Comment.query().fetch()
        self.response.write(haiku_page.render(
            haikus=haikus,
            signedin_username=signedin_username,
            Comment=model.Comment))

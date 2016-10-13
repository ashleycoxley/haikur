from handler_helper import HaikurHandler
import model
from helper.user_validation import *
from helper.global_vars import *


class MainPageHandler(HaikurHandler):
    def get(self):
        signedin_username = self.get_username_by_cookie()
        if signedin_username is None:
            signedin_username = ""
        haikus = model.Haiku.query().order(-model.Haiku.created_date)
        if haikus.count() == 0:
            empty_page = JINJA_ENV.get_template('/base.html')
            self.response.write(empty_page.render(
                signedin_username=signedin_username,
                header_color=DEFAULT_COLOR))
            return
        
        for haiku in haikus:
            header_color = haiku.color
            break
        haiku_page = JINJA_ENV.get_template('/haiku.html')
        self.response.write(haiku_page.render(
            header_color=header_color,
            haikus=haikus,
            signedin_username=signedin_username,
            Comment=model.Comment))

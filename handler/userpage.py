from handler_helper import HaikurHandler
from helper.global_vars import JINJA_ENV
import model

class UserPageHandler(HaikurHandler):
    def get(self, collection_username):
        haikus = model.Haiku.query(model.Haiku.username==collection_username).order(-model.Haiku.created_date)
        for haiku in haikus:
            header_color = haiku.color
            break
        signedin_username = self.get_username_by_cookie()
        if signedin_username is None:
            signedin_username = ""
        haiku_page = JINJA_ENV.get_template('/haiku.html')
        self.response.write(haiku_page.render(
            header_color=header_color,
            haikus=haikus,
            signedin_username=signedin_username,
            Comment=model.Comment))
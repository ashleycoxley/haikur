from handler_helper import HaikurHandler
from helper.global_vars import JINJA_ENV
from google.appengine.ext import ndb


class SingleHaikuHandler(HaikurHandler):
    def get(self, haiku_id):
        signedin_username = self.get_username_by_cookie()
        if signedin_username is None:
            signedin_username = ""
        haiku_key = ndb.Key('Haiku', int(haiku_id))
        haiku = haiku_key.get()

        if not haiku:
            self.error(404)
            return

        header_color = haiku.color
        single_haiku_page = JINJA_ENV.get_template('permalink.html')
        self.response.write(single_haiku_page.render(
            signedin_username=signedin_username,
        	haiku=haiku,
        	header_color=header_color))

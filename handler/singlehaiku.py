from handler_helper import HaikurHandler
from helper.global_vars import JINJA_ENV
from google.appengine.ext import ndb

class SingleHaikuHandler(HaikurHandler):
    def get(self, haiku_id):
        haiku_key = ndb.Key('Haiku', int(haiku_id))
        haiku = haiku_key.get()

        if not haiku:
            self.error(404)
            return

        single_haiku_page = JINJA_ENV.get_template('permalink.html')
        self.response.write(single_haiku_page.render(haiku=haiku))

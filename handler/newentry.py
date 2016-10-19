from handler_helper import HaikurHandler
import model
from helper.global_vars import *
from helper.haiku_validation import *

from google.appengine.ext import ndb


class NewEntryHandler(HaikurHandler):
    def get(self):
        signedin_username = self.get_username_by_cookie()
        if signedin_username:
            entry_form = JINJA_ENV.get_template('newentry.html')
            self.response.write(entry_form.render(
                header_color=DEFAULT_COLOR,
                signedin_username=signedin_username,
                red="checked='checked'",
                edit=False
                ))
        else:
            self.redirect('/signin')

    def post(self):
        user_id = self.read_user_cookie()
        if not user_id:
            self.redirect('/signin')

        stanza1 = self.request.get('stanza1')
        stanza2 = self.request.get('stanza2')
        stanza3 = self.request.get('stanza3')
        color = self.request.get('haiku-color')

        form_valid, template_values = validate_haiku([
            stanza1,
            stanza2,
            stanza3
            ])

        if form_valid:
            width = set_width(stanza1, stanza2, stanza3)
            haiku = model.Haiku(
                user_key=model.User.get_by_id(int(user_id)).key,
                username=model.User.get_by_id(int(user_id)).username,
                stanza1=stanza1,
                stanza2=stanza2,
                stanza3=stanza3,
                color=color,
                width=width
                )
            haiku_key = haiku.put()
            haiku_id = str(haiku_key.id())

            self.redirect('/' + haiku_id)

        else:
            entry_form = JINJA_ENV.get_template('newentry.html')
            self.response.write(entry_form.render(
                signedin_username=signedin_username,
                stanza1=template_values['stanza1'],
                stanza2=template_values['stanza2'],
                stanza3=template_values['stanza3'],
                stanza1_error=template_values['stanza1_error'],
                stanza2_error=template_values['stanza2_error'],
                stanza3_error=template_values['stanza3_error']))

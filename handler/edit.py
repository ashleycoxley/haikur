from handler_helper import HaikurHandler
import model
from helper.global_vars import *
from helper.haiku_validation import *

from google.appengine.ext import ndb
import datetime


class EditHandler(HaikurHandler):
    def get(self, haiku_id):
        haiku = model.Haiku.get_by_id(int(haiku_id))
        if not haiku:
            self.redirect('/')
        stanza1 = haiku.stanza1
        stanza2 = haiku.stanza2
        stanza3 = haiku.stanza3            
        signedin_username = self.get_username_by_cookie()
        if signedin_username:
            entry_form = JINJA_ENV.get_template('newentry.html')
            self.response.write(entry_form.render(
                signedin_username=signedin_username,
                stanza1=stanza1,
                stanza2=stanza2,
                stanza3=stanza3
                ))
        else:
            self.redirect('/signin')

    def post(self, haiku_id):
        user_id = self.read_user_cookie()
        if not user_id:
            self.redirect('/signin')

        new_stanza1 = self.request.get('stanza1')
        new_stanza2 = self.request.get('stanza2')
        new_stanza3 = self.request.get('stanza3')
        new_color = self.request.get('haiku-color')

        form_valid, template_values = validate_haiku([
            new_stanza1,
            new_stanza2,
            new_stanza3
            ])

        if form_valid:
            haiku = model.Haiku.get_by_id(int(haiku_id))
            haiku.stanza1 = new_stanza1
            haiku.stanza2 = new_stanza2
            haiku.stanza3 = new_stanza3
            haiku.color = new_color
            haiku.edited_date = datetime.datetime.now()

            haiku_key = haiku.put()

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

        


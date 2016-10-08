from handler_helper import HaikurHandler
import model
from helper.global_vars import *

from google.appengine.ext import ndb


def validate_haiku(haiku_list):
    template_values = {
        'stanza1': '',
        'stanza2': '',
        'stanza3': ''
        }

    form_valid = False
    template_values['stanza1_error'] = stanza_invalid(haiku_list[0], 5)
    template_values['stanza2_error'] = stanza_invalid(haiku_list[1], 7)
    template_values['stanza3_error'] = stanza_invalid(haiku_list[2], 5)

    if template_values['stanza1_error'] == "":
        template_values['stanza1'] = haiku_list[0]
    if template_values['stanza2_error'] == "":
        template_values['stanza2'] = haiku_list[1]
    if template_values['stanza3_error'] == "":
        template_values['stanza3'] = haiku_list[2]

    if template_values['stanza1_error'] == "" and template_values['stanza2_error'] == "" and template_values['stanza3_error'] == "":
        form_valid = True

    return form_valid, template_values


def stanza_invalid(stanza, syllable_count):
    # This will return '' if valid, and an error string if invalid:
    # HAIKU_ERROR['incomplete'] if it's empty
    # HAIKU_ERROR['syllables'] if syllables are 'wrong'
    if not stanza:
        return HAIKU_ERROR_MESSAGES['incomplete']
    else:
        return ""


class NewEntryHandler(HaikurHandler):
    def get(self):
        signedin_username = self.get_username_by_cookie()
        if signedin_username:
            entry_form = JINJA_ENV.get_template('newentry.html')
            self.response.write(entry_form.render(
                signedin_username=signedin_username))
        else:
            self.redirect('/login')

    def post(self):
        user_id = self.read_user_cookie()
        if not user_id:
            self.redirect('/login')

        stanza1 = self.request.get('stanza1')
        stanza2 = self.request.get('stanza2')
        stanza3 = self.request.get('stanza3')

        form_valid, template_values = validate_haiku([
            stanza1,
            stanza2,
            stanza3
            ])

        if form_valid:
            haiku = model.Haiku(
                user_key=model.User.get_by_id(int(user_id)).key,
                username=model.User.get_by_id(int(user_id)).username,
                stanza1=stanza1,
                stanza2=stanza2,
                stanza3=stanza3,
                )
            haiku_key = haiku.put()
            haiku_id = str(haiku_key.id())

            self.redirect('/' + haiku_id)

        else:
            entry_form = JINJA_ENV.get_template('newentry.html')
            self.response.write(entry_form.render(
                stanza1=template_values['stanza1'],
                stanza2=template_values['stanza2'],
                stanza3=template_values['stanza3'],
                stanza1_error=template_values['stanza1_error'],
                stanza2_error=template_values['stanza2_error'],
                stanza3_error=template_values['stanza3_error']))

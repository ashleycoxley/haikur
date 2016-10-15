from handler_helper import HaikurHandler
import model
from helper.global_vars import *

from google.appengine.ext import ndb


def delete_haiku(haiku_id):
    haiku = model.Haiku.get_by_id(int(haiku_id))
    comment_keys = model.Comment.query(model.Comment.haiku_ref==haiku.key).iter(keys_only=True)
    ndb.delete_multi(comment_keys)
    haiku.key.delete()


class DeleteHaikuHandler(HaikurHandler):
    def get(self, haiku_id):
    	signedin_username = self.get_username_by_cookie()
    	haiku_author = model.Haiku.get_by_id(int(haiku_id)).username
    	if signedin_username is None or signedin_username != haiku_author:
    		self.redirect('/')
        else:
            delete_haiku(haiku_id)
            self.redirect('/')

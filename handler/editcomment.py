from handler_helper import HaikurHandler
import model
from helper.global_vars import *

from google.appengine.ext import ndb
import datetime


class EditCommentHandler(HaikurHandler):
    def post(self, haiku_id, comment_id):
        user_id = self.read_user_cookie()
        signedin_username = self.get_username_by_cookie()
        comment = model.Comment.get_by_id(int(comment_id))

        if signedin_username != comment.username:
            self.abort(403)

        edited_text = self.request.get('editedText')

        comment.comment_text = edited_text
        comment.edited_date = datetime.datetime.now()

        comment_key = comment.put()

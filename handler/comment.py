from handler_helper import HaikurHandler
import model
from helper.global_vars import *

from google.appengine.ext import ndb
import json


class CommentHandler(HaikurHandler):
    def post(self, haiku_id):
        user_id = self.read_user_cookie()
        if self.not_signed_in(user_id):
            self.abort(403)
        signedin_username = self.get_username_by_cookie()
        comment_text = self.request.get('commentText')
        haiku_id = self.request.get('haikuID')
        haiku_key = ndb.Key('Haiku', int(haiku_id))

        if comment_text:
            comment = model.Comment(
                haiku_ref=haiku_key,
                user_key=model.User.get_by_id(int(user_id)).key,
                username=signedin_username,
                comment_text=comment_text
                )
            comment_key = comment.put()
            comment_response = {'commentID': comment_key.id()}
            self.response.write(json.dumps(comment_response))

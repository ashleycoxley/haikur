from handler_helper import HaikurHandler
import model
from google.appengine.ext import ndb

class CommentHandler(HaikurHandler):
    def post(self, haiku_id):
        user_id = self.read_user_cookie()
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

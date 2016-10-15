from handler_helper import HaikurHandler
import model
from google.appengine.ext import ndb

def delete_comment(comment_id):
    comment = model.Comment.get_by_id(int(comment_id))
    comment.key.delete()
    print comment_id, 'deleted'


class DeleteCommentHandler(HaikurHandler):
    def post(self, haiku_id, comment_id):
    	signedin_username = self.get_username_by_cookie()
    	comment_author = model.Comment.get_by_id(int(comment_id)).username
    	if signedin_username is None or signedin_username != comment_author:
    		return
    	else:
        	delete_comment(comment_id)
        	self.redirect('/')

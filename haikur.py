import webapp2
import logging
import handler

logging.basicConfig(level=logging.INFO)

app = webapp2.WSGIApplication([
    ('/', handler.MainPageHandler),
    ('/newpost', handler.NewEntryHandler),
    ('/signup', handler.SignupHandler),
    ('/signin', handler.LoginHandler),
    ('/signout', handler.LogoutHandler),
    ('/user/(\w+)', handler.UserPageHandler),
    ('/(\d+)/comment', handler.CommentHandler),
    ('/(\d+)/vote', handler.VoteHandler),
    ('/(\d+)', handler.SingleHaikuHandler),
    ])

import webapp2
import logging
import handler

logging.basicConfig(level=logging.INFO)



app = webapp2.WSGIApplication([
    ('/', handler.MainPageHandler),
    ('/newpost', handler.NewEntryHandler),
    ('/signup', handler.SignupHandler),
    ('/login', handler.LoginHandler),
    ('/logout', handler.LogoutHandler),
    ('/(\w+)/comment', handler.CommentHandler),
    ('/(\w+)', handler.SingleHaikuHandler)
    ])


import webapp2

from security import Root

from controllers import home
from controllers import signup
from controllers import signin



class fundr(Root.Handler):
    def get(self):
        self.redirect('/home')



app = webapp2.WSGIApplication([
    ('/',			fundr),
    ('/home',		home.Home),
    ('/signin',		signin.Signin)
    ('/signup',		signup.Signup),
  
], debug=True)          # CHANGE TO False BEFORE FINAL DEPLOYMENT
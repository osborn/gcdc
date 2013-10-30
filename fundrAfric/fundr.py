
import webapp2

from security import Root

from controllers import home
from controllers import signup
from controllers import signin
from controllers import create
from controllers import discover



class fundr(Root.Handler):
    def get(self):
        self.redirect('/home')

class page_not_found(Root.Handler):
	def get(self):
		self.render('404.html')



app = webapp2.WSGIApplication([
    ('/',			fundr),
    ('/home',		home.Home),
    ('/signin',		signin.Signin),
    ('/signup',		signup.Signup),
    ('/create', 	create.Create),
    ('/discover',   discover.Discover),
    ('/404_not_found', page_not_found),
  
], debug=True)          # CHANGE TO False BEFORE FINAL DEPLOYMENT
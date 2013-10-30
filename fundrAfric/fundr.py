
import webapp2

from security import Root
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import urlfetch
from models import Destination, Tourist, Guide, Request
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler


class fundr(Root.Handler):
    def get(self):
        self.redirect('/home')

class Home(Root.Handler):
    def get(self):
        self.render("index.html")

class Signup(Root.Handler):
    def get(self):
        if self.check_session("query"):
            self.redirect("/home")
        else:
            self.render("signup.html")

    def post(self):
        email = self.request.get("email")
        password = self.request.get("password")
        confirm_password  = self.request.get("confirm_password")
        picture_fetch = urlfetch.Fetch("http://s3.amazonaws.com/37assets/svn/765-default-avatar.png")
        picture = picture_fetch.content
        all_users = Tourist.Tourist.all()

        if email and password and confirm_password:
            if self.validate_email(email) and self.validate_password(password) and password == confirm_password and (self.get_user_by_email(all_users, email) == None):
                # tourist_obj = Tourist.Tourist(username = username, password = password, email = email)
                _args = {"name":email, "password":password}
                hashed_password, salt = self.hash_password(_args)
                token, salt2 = self.hash_password(_args)
                tourist = Tourist.Tourist.addTourist(email, hashed_password, salt, token, picture)

                session_vars = {"name" : "authenticator", "value" : email}
                session_vars2 = {"name" : "query", "value" : tourist.key().id()}
                self.create_session(session_vars)
                self.create_session(session_vars2)

                ph = "lkdsjfdsjklfjhiwereyim,nn.nafndfgityereryewiybx,ncn,neroejslfjoiuer"
                _args = {"name":email + ph, "password":password}
                verification_link = "http://tourbly.appspot.com/verify_email?token=" + token + "&id=" + str(tourist.key().id())
                params = {"email" : email, "url" : verification_link}
                self.send_verification_email(params)
                self.render("home.html", test = "You have Signed up successfully, " + tourist.email)
            else:
                self.render("signup.html", email = email, email_error = self.email_error_prompt(email), 
                    password_error = self.password_error_prompt(password), confirm_password_error = 
                    self.confirm_password_error_prompt(password, confirm_password))
        else:
            error = "All fields are required"
            self.render("signup.html", email = email, error = error)


class Signin(Root.Handler):
    def get(self):
        if self.check_session("query"):
            self.redirect("/home")
        else:
            self.render("signin.html")

    def post(self):
        email = self.request.get("email")
        password = self.request.get("password")
        all_users = Tourist.Tourist.all()
        # tourist = self.get_user_by_email(all_users, email)
        tourist = db.GqlQuery("select * from Tourist where email = :1", email).get()

        if email and password:
            if tourist:
                hashed_password= tourist.password
                salt = tourist.salt
                _args = {"password" : password, "hashed_password" : hashed_password, "salt" : salt}
                if self.auth_password(_args):
                    session_vars = {"name" : "authenticator", "value" : email}
                    session_vars2 = {"name" : "query", "value" : tourist.key().id()}
                    self.create_session(session_vars)
                    self.create_session(session_vars2)

                    if tourist.first_name == None:
                        self.render("home.html", test = "You've been signed in successfully, " + tourist.email)
                    else:
                        self.render("home.html", test = "You've been signed in successfully, " + tourist.firstName)
                else:
                    self.render("signin.html", error = "Invalid email or password")
            else:
                self.render("signin.html", error = "User with email " + email + " cannot be found")
        else:
            self.render("signin.html", error = "Both fields are required")


class Logout(Root.Handler):
     def get(self):
        current_page = self.request.get("current_page")
        self.logout(["authenticator", "query"])
        self.redirect("/" + current_page)

class VerifyEmailhandler(Root.Handler):
    def get(self):
        token = self.request.get("token")
        tourist_id = int(self.request.get("id"))
        tourist = Tourist.Tourist.get_by_id(tourist_id)

        if tourist.token == token:
            tourist.activated = True
            tourist.put()
            self.render("profile.html", success_message = "Your account has been activated")
        else: 
            self.redirect("/home")

class ImageHandler(Root.Handler):
    def get(self):
        tourist_id = int(self.request.get('tourist_id'))
        tourist = Tourist.Tourist.get_by_id(tourist_id)
        if tourist.picture:
            self.response.headers['Content-Type'] = 'image/png'
            self.write(tourist.picture)

class profileHandler(Root.Handler):
    def get(self):
        if self.check_session("query"):
            tourist_id = int(self.get_cookie("query")[0])
            tourist = Tourist.Tourist.get_by_id(tourist_id)
            self.render("profile.html", email = tourist.email, first_name = tourist.first_name, 
                last_name = tourist.last_name, country = tourist.country, state = tourist.state, 
                tourist_id = tourist_id, isLoggedIn = self.check_session("query"), tourist = tourist)
        else:
            self.redirect("/home")

    def post(self):
        tourist_id = int(self.get_cookie("query")[0])
        tourist = Tourist.Tourist.get_by_id(tourist_id)

        new_email = self.request.get("email")
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        country = self.request.get("country")
        state = self.request.get("state")
        picture = self.request.get("profile_pic")

        if self.validate_email(new_email) and self.validate_name(first_name) and self.validate_name(last_name):
            Tourist.Tourist.updateTourist(tourist, new_email, first_name, last_name, country, state)
            if picture:
                tourist.picture = str(picture)
                tourist.put()
            self.render("profile.html", email = tourist.email, first_name = tourist.first_name, 
                last_name = tourist.last_name, country = tourist.country, state = tourist.state, isLoggedIn = self.check_session("query"),
                tourist_id = tourist_id, success_message = "Your profile has been updated successfully", tourist = tourist)
        else:
            self.render("profile.html", email = new_email, email_error = self.profile_email_error_prompt(tourist.email, new_email), first_name = 
                first_name, last_name = last_name, state = state, tourist_id = tourist_id, success_message = "there is something wrong")


  

app = webapp2.WSGIApplication([
    ('/', fundr),
    ('/home', Home),
    ('/signup', Signup),
    ('/signin', Signin),
    ('/logout', Logout),
  
], debug=True)          # CHANGE TO FALSE BEFORE FINAL DEPLOYMENT
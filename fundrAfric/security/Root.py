# @name    Root.py
# @author  Samuel A.
# @date    Oct 13 13
# @purpose assorted features, read code docs below


import os
import re
import cgi
import hmac
import random
import string
import jinja2
import webapp2
import datetime

    
## Globals

ph           = 'squemishossifragealladinandthemagiclampallinanutshellTheEndIsNighAndAllMustPrepare'
template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env    = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)





## => Implements various utility functions for handling security operations

class Security():

    # Name - Hash_string
    # Desc
    #   Makes a hash of any string using a secret key
    # params
    #   self  : Ref    -> reference to object instance
    #   ref   : String -> value to be hashed
    # returns
    #   : String -> hashed version of string ref

    def Hash_string(self, ref):
        cypher = hmac.new(ph, str(ref))
        return cypher.hexdigest()
    

    # Name - hash_password
    # Desc
    #   encrypts passwords by hashing with a uniquely generated salt
    #   combined with the secret key
    # params
    #   self  : Ref    -> reference to object instance
    #   _args : Object :: name     : String  -> name of user (used to generate unique salt)
    #                  :: password : String  -> password to be encrypted
    # returns
    #   :String -> hashed password and random salt

    def hash_password(self, _args):
        salt = self.rand_salt(_args['name'])
        hash_pass = hmac.new(salt+ph, str(_args['password']))
        return hash_pass.hexdigest(), salt
        # salt = self.rand_salt(_args.name)
        # hash_pass = hmac.new(salt+ph, str(_args.password))
        # return hash_pass.hexdigest(), salt
        

    # Name - auth_password
    # Desc
    #   verifies passwords by hashing and comparing with stored hash
    # params
    #   self  : Ref    -> reference to object instance
    #   _args : Object :: salt       : String  -> stored salt
    #                  :: plainPass  : String  -> password to be verified
    #                  :: hashedPass : String  -> stored hash of password
    # returns
    #   : Boolean -> True if matched, False otherwise
        
    def auth_password(self, _args):
        if hmac.new(_args["salt"]+ph, str(_args["password"])).hexdigest() == _args["hashed_password"]:
            return True
        else:
            return False



    # Name - auth_hash
    # Desc
    #   compares plain string to hash for possible match (used to check for tamparing)
    # params
    #   self  : Ref    -> reference to object instance
    #   _args : Object :: plainStr  : String  -> plain text to be verified
    #                  :: hashedStr : String  -> hashed string for integrity check
    # returns
    #   : Boolean -> True if matched, False otherwise

    def auth_hash(self, plain, cypher):
        if cypher == self.Hash_string(plain):
            return True
        else:
            return False
        


    # Name - rand_salt
    # Desc
    #   generates a random salt using a given string as base
    # params
    #   self  : Ref    -> reference to object instance
    #   _args : Object :: base  : String  -> base string used to generate salt
    # returns
    #   : String -> the generated salt

    def rand_salt(self, _args):
        return ''.join(random.choice(_args) for i in range(8)) 
        + ''.join(random.choice(string.letters) for i in range(8))







# => Request handler extended with class Security and misc functionality
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{0,20}$")
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
PASS_RE = re.compile(r"^.{6,20}$")


class Handler(Security, webapp2.RequestHandler):
    
    def w(cls,*a, **kw):
        Handler.response.out.write(*a, **kw)
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
        
    # standard render function
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def handle_exception(self, exception, debug):
        # Set a custom message.
        self.render('404.html')

        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)
    

    # Name - validate_name
        # Desc
        #   Validates name enterd by user for signup
        # params
        #   name  : name entered by user
        # returns
        #   : Boolean -> Valid name or invalid
    @staticmethod
    def validate_name(name):
        if re.match(USER_RE, name):
            return True
        else:
            return False
            
            
    # Name - validate_password
        # Desc
        #   Validates password enterd by user for signup
        # params
        #   self           : Ref    -> reference to object instance
        #   username  : password entered by user
        # returns
        #   : Boolean -> Valid password or invalid
    @staticmethod
    def validate_password(password):
        if re.match(PASS_RE, password):
            return True
        else:
            return False
            
    #validates email input
    @staticmethod
    def validate_email(email):
        if re.match(EMAIL_RE, email):
            return True
        else:
            return False

    # Name - set_cookie
    # Desc
    #   Sets a cookie given the name and value
    # params
    #   self  : Ref    -> reference to object instance
    #   _args : object :: name       : String  -> name of cookie
    #                  :: value      : String  -> contents of cookie
    #                  :: [validity] : Integer -> validity period of cookie default=4wks
    # returns
    #   : Void -> returns nothing

    def set_cookie(self, _args):
        self.response.headers.add_header('Set-Cookie', '%s=%s|%s; expires=%s' % 
             (str(_args["name"]), str(_args["value"]), self.Hash_string(_args["value"]), 
              (datetime.datetime.now()
              + datetime.timedelta(weeks=_args["validity"] | 4)).strftime('%a, %d %b %Y %H:%M:%S GMT')))
        


    # Name - logout
    # Desc
    #   Closes the current session by clearing login cookies
    # params
    #   self        : Ref    -> reference to object instance
    #   cookie_list : List   -> list of cookies to be unset
    # returns
    #   : Void -> returns nothing

    def logout(self, cookie_list):
        for cookie in cookie_list:
            self.response.headers.add_header('Set_Cookie', '%s=' %(cookie))


    # Name - get_cookie
    # Desc
    #   retrieves the value of a given cookie
    # params
    #   self        : Ref    -> reference to object instance
    #   name  : String -> name of cookie to be retrieved
    # returns
    #   : List -> list containing a plain text cookie and it's hash or [None, None] if not found

    def get_cookie(self, name):
        cookie = self.request.cookies.get(name, None)
        
        if cookie:
            temp = cookie.split('|')
            return temp
        else:
            return [None, None]
    


    # Name - get_cookie ==> (Deprecated)
    # Desc
    #   retrieves the value of a given cookie
    # params
    #   self : Ref    -> reference to object instance
    #   name : String -> name of cookie to be retrieved
    # returns
    #   : 

    def get_user_id(self):
        cookie = self.request.cookies.get('query', None)
        return int(cookie.split('|')[0])
    


    # Name - create_session
    # Desc
    #   creates a user session by setting appropriate cookies
    # params
    #   self         : Ref  -> reference to object instance
    #   session_vars : List -> list of objects with cookie name and value as follows
    #                           :: name  -> name of cookie
    #                           :: value -> value of cookie
    # returns
    #   : Void -> returns nothing
    def create_session(self, session_vars):
        # # for cookie in session_vars:
        #     self.set_cookie(cookie["name"], cookie["value"])
        _args = {"name" : session_vars["name"], "value" : session_vars["value"], "validity" : 4}
        self.set_cookie(_args)
        
        
    # Name - check_session
    # Desc
    #   verifies client's login status
    # params
    #   self           : Ref    -> reference to object instance
    #   session_cookie : String -> name of session cookie
    # returns
    #   : Boolean -> True if user is logged in, False otherwise

    def check_session(self, session_cookie):
        session = self.get_cookie(session_cookie)
        return self.auth_hash(session[0], session[1])

    # Name - get_user_by_email
    # Desc
    #   Gets a user by the email
    # params
    #   self           : Ref    -> reference to object instance
    #   all_users : objects of all users in the table in question
    #   email : Email to be used for the query
    # returns
    #   : User -> User if that email exists, none if otherwise

    def get_user_by_email(self, all_users, email):
        return all_users.filter("email =", email).get()

    # Name - username
    # Desc
    #   Gets a user by the username
    # params
    #   self           : Ref    -> reference to object instance
    #   all_users : objects of all users in the table in question
    #   username : Username to be used for the query
    # returns
    #   : User -> User if that username exists, none if otherwise
    def get_user_by_username(self, all_users, username):
        return all_users.filter("username =", username).get()

    # Name - username_error_prompt
    # Desc
    #   To get the right error prompt to be displayed to the user when username is enterd for signup
    # params
    #   self           : Ref    -> reference to object instance
    #   username : Username entered by user for signup
    # returns
    #   : String -> Error prompt to the user
    def username_error_prompt(self, username):
        all_users = Tourist.Tourist.all()
        if username == "":
            return "Username is required"
        elif self.validate_username(username) != True:
            return "Username must be at least 3 characters"
        elif self.get_user_by_username(all_users, username) != None:
            return "Username already exists"
        else:
            return ""


    # Name - email_error_prompt
    # Desc
    #   To get the right error prompt to be displayed to the user when email is enterd for signup
    # params
    #   self           : Ref    -> reference to object instance
    #   email : Email entered by user for signup
    # returns
    #   : String -> Error prompt to the user
    def email_error_prompt(self, email):
        all_users = Tourist.Tourist.all()
        if email == "":
            return "Email is required"
        elif self.validate_email(email) != True:
            return "Inavid email entered"
        elif self.get_user_by_email(all_users, email) != None:
            return "Email already exists"
        else:
            return ""

    # Name - profile_email_error_prompt
    # Desc
    #   To get the right error prompt to be displayed to the user when email is enterd for signup
    # params
    #   self           : Ref    -> reference to object instance
    #   email : Email entered by user for signup
    # returns
    #   : String -> Error prompt to the user
    def profile_email_error_prompt(self, email, new_email):
        all_users = Tourist.Tourist.all()
        if new_email == "":
            return "Email is required"
        elif self.validate_email(new_email) != True:
            return "Inavid email entered"
        elif self.get_user_by_email(all_users, new_email) != None and new_email != email:
            return "Email already exists"
        else:
            return ""
        

    # Name - password_error_prompt
    # Desc
    #   To get the right error prompt to be displayed to the user when password is enterd for signup
    # params
    #   self           : Ref    -> reference to object instance
    #   password : Password entered by user for signup
    # returns
    #   : String -> Error prompt to the user
    def password_error_prompt(self, password):
        if password == "":
            return "Password is required"
        elif self.validate_password(password) != True:
            return "Password must be at least 6 characters"
        else:
            return ""

    def confirm_password_error_prompt(self, password, confirm_password):
        if confirm_password == "":
            return "Confirm Your Password"
        elif confirm_password != password:
            return "Passwords do not match"
        else:
            return ""

    # Name - send_verification_email
    # Desc
    #   To get the right error prompt to be displayed to the user when password is enterd for signup
    # params
    #   self           : Ref    -> reference to object instance
    #   _args : List -> list of objects with cookie name and value as follows
    #                           :: email  -> Email of user to which verification message will be sent
    #                           :: url -> link with token to verify user's email
    # returns
    #   : Void -> Returns nothing
    def send_verification_email(self, _args):
        message = mail.EmailMessage(sender="Christian Osei-Bonsu <christian.osei-bonsu@meltwater.org>",
                            subject="Welcome To Tourbly, Please Verify Your Account")

        message.to = "<" + _args["email"] + ">"
        message.body = """
        Dear User:

        You have successfully signed up onto the Tourbly platform. Discover beautiful scenery, 
        culture and lifestyles with friendly and reliable tour guides you can trust.

        Please complete your sign up by clicking on the following link """ + _args["url"] + """

        Cheers,
        The Tourbly Team
        """

        message.send()


        
        
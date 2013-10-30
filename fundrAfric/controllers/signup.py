from security import Root

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
        picture_fetch = urlfetch.Fetch("http://s3.amazonaws.com/37/assets/svn/765-default-avatar.png")
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
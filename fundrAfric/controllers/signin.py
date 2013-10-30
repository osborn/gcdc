
from security import Root


class Signin(Root.Handler):
    def get(self):
        self.render("signin.html")
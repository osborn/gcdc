
from security import Root


class Signup(Root.Handler):
    def get(self):
        self.render("signup.html")
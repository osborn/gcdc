
from security import Root


class Discover(Root.Handler):
    def get(self):
        self.render("discover.html")
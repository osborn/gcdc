
from security import Root


class Home(Root.Handler):
    def get(self):
        self.render("index.html")
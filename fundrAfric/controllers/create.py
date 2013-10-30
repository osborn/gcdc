
from security import Root


class Create(Root.Handler):
    def get(self):
        self.render("create.html")
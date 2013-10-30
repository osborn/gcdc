# @name    Review.py
# @author  Samuel A.
# @date    Oct 13 13
# @purpose db model for Review data


from security import Root
from google.appengine.ext import db

date = ""

class Review(db.Model, Root.Handler):
    _reviewer = db.StringProperty()
    _reviewee = db.StringProperty()
    _rating   = db.IntegerProperty()
    _comment  = db.StringProperty()


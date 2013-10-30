# @name    Donner
# @author  Samuel A.
# @date    Oct 11 13
# @purpose db model for donner data


from security import Root
from pyscripts import Utility
import Review
from google.appengine.ext import db


class Donner(db.Model, Root.Handler):
    _name       = db.StringProperty()
    _date       = db.DateTimeProperty()
    _amount     = db.StringProperty()
    _campaign   = db.ReferenceProperty()
    _location   = db.LatLngProperty()

# @name    Request.py
# @author  Samuel A.
# @date    Oct 13 13
# @purpose db model for Request data


from security import Root
import Destination
import Guide
from google.appengine.ext import db

date = ""

class Request(db.Model, Root.Handler):
    _destination = db.ReferenceProperty(Destination.Destination)
    _startDate   = db.DateTimeProperty()
    _requester   = db.ListProperty(db.Key)
    _endDate     = db.DateTimeProperty()
    _guide       = db.ReferenceProperty(Guide.Guide)
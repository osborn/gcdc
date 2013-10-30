# @name    Guide.py
# @author  Samuel A.
# @date    Oct 11 13
# @purpose db model for Guide data


from security import Root
from pyscripts import Utility
import Review
from google.appengine.ext import db


date = ""

class Guide(db.Model, Root.Handler):
    _firstname   = db.StringProperty()
    _lastname    = db.StringProperty()
    _email       = db.EmailProperty()
    _phoneNumber = db.PhoneNumberProperty()
    _dateOfBirth = db.DateProperty()
    _locations   = db.ListProperty(db.Key)
    _workDays    = db.ListProperty(db.Key)
    _picture     = db.BlobProperty()
    _languages   = db.ListProperty(db.Key)
    _rating      = db.ReferenceProperty(Review.Review, collection_name='reviews')

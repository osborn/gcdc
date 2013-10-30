# @name    User
# @author  Samuel A.
# @date    Oct 11 13
# @purpose db model for user data


import campaign

from security import Root
from pyscripts import Utility
from google.appengine.ext import db


class User(db.Model, Root.Handler):
    _address     = db.TextProperty()        # Check if Address property exists
    _email       = db.EmailProperty()
    _firstname   = db.StringProperty()
    _lastname    = db.StringProperty()
    _phoneNumber = db.PhoneNumberProperty()
    _campaigns   = db.ReferenceProperty(campaign.Campaign, collection_name="campaigns")

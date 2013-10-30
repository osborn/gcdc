# @name    Campaign
# @author  Samuel A.
# @date    Oct 11 13
# @purpose db model for campaign data


from security import Root
from pyscripts import Utility
from google.appengine.ext import db


class Campaign(db.Model, Root.Handler):
    _name 	     	= db.StringProperty()
    _organisation	= db.StringProperty()
    _category       = db.StringProperty()
    _targetAmount 	= db.StringProperty()
    _startDate 		= db.DateProperty()
    _endDate 		= db.DateProperty()
    _description   	= db.TextProperty()
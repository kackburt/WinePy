from google.appengine.ext import ndb

class WineData(ndb.Model):
    category = ndb.StringProperty()
    color = ndb.StringProperty()
    sweetness = ndb.StringProperty()
    country = ndb.StringProperty()
    region = ndb.StringProperty()
    winery = ndb.StringProperty()
    name = ndb.StringProperty()
    vine = ndb.StringProperty()
    year = ndb.IntegerProperty()
    amount = ndb.IntegerProperty()
    unit = ndb.StringProperty()
    image = ndb.BlobKeyProperty()
    tried = ndb.BooleanProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
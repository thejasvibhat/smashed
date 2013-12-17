import webapp2

import uuid
import cgi
import urllib
from webapp2_extras import auth, sessions
import os
from google.appengine.api import users

from google.appengine.ext import ndb
from google.appengine.api import search
import storereview

from User.handlers import AuthHandler
_INDEX_NAME = 'localityTagSearch'
REVIEW_DB_NAME = 'bars_location_db'
def review_dbkey(review_dbname=REVIEW_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('bars_db_review', review_dbname) 


class LocationDb(ndb.Model):
    addressid = ndb.StringProperty()
    lat = ndb.StringProperty()
    lng = ndb.StringProperty()
    formattedaddress = ndb.StringProperty()
    locality = ndb.StringProperty()
    city = ndb.StringProperty()
    pincode = ndb.StringProperty()    

def tokenize_autocomplete(phrase):
    a = []
    for word in phrase.split():
        j = 1
        while True:
            a.append(word[0:0 + j])
            if j == len(word):
                break
            j += 1
    return a

def CreateDocument(city,locality, pincode,barname,bid):
    """Creates a search.Document from content written by the author."""
    # Let the search service supply the document id.
    address = ','.join(tokenize_autocomplete(locality))
    name = ','.join(tokenize_autocomplete(barname))
    return search.Document(
        fields=[search.TextField(name='tagsAddress', value=address),
                search.TextField(name='tagsName', value=name),
				search.TextField(name='locality', value=locality),
                search.TextField(name='name', value=barname),
                search.TextField(name='pincode', value=pincode),
                search.TextField(name='city', value=city),
                search.TextField(name='bid', value=bid)
                ]) 

def CreateAddress (reviewDict,bid):
    location = LocationDb(parent=review_dbkey(REVIEW_DB_NAME))
    location.addressid = str(uuid.uuid4())
    location.lat = reviewDict.get('lat')
    location.lng = reviewDict.get('long')
    location.formattedaddress = reviewDict.get('address')
    location.locality = reviewDict.get('locality')
    location.city = reviewDict.get('area1')
    location.pincode = reviewDict.get('zip')
    search.Index(name=_INDEX_NAME).put(CreateDocument("Bengaluru", location.locality,location.pincode,reviewDict.get('name'),bid))
    location.put()
    
    return (str(location.addressid),str(location.formattedaddress))
        
 

import os
import webapp2
import urllib2
import json
from datetime import datetime
from google.appengine.ext import ndb
import logging
from google.appengine.api import search
_INDEX_NAME = 'localityTagSearch'
class RegionDb(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    city    = ndb.StringProperty()
    locality = ndb.StringProperty()
    pincode   = ndb.StringProperty()

def tokenize_autocomplete(phrase):
    a = []
    for word in phrase.split():
        j = 1
        while True:
            for i in range(len(word) - j + 1):
                a.append(word[i:i + j])
            if j == len(word):
                break
            j += 1
    return a

def CreateDocument(city,locality, pincode):
    """Creates a search.Document from content written by the author."""
    # Let the search service supply the document id.
    name = ','.join(tokenize_autocomplete(locality))
    return search.Document(
        fields=[search.TextField(name='tags', value=name),
				search.TextField(name='locality', value=locality),
                search.TextField(name='pincode', value=pincode),
                search.TextField(name='city', value=city),
                search.DateField(name='date', value=datetime.now().date())])
  
class PushLocality(webapp2.RequestHandler):
    def get(self):
        fileOpen = open('region1.txt','r')
        logging.info('here')
        dataString = fileOpen.read()
        spl = dataString.split(';')
        for combo in spl:
            logging.info('%s' %combo)
            locPin = combo.split(":")
            search.Index(name=_INDEX_NAME).put(CreateDocument("Bengaluru", locPin[0],locPin[1]))
            #rdb = RegionDb(parent=ndb.Key('r_db', 'r_db'))
            #rdb.city = "Bengaluru"
            #rdb.locality = locPin[0]
            #rdb.pincode = locPin[1]
            #rdb.put()
        

         

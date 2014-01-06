import webapp2
import urllib

from google.appengine.ext import ndb

from google.appengine.api import images

from google.appengine.ext import db

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from User.handlers import AuthHandler

MEME_DB_NAME = 'meme_db'

def meme_dbkey(meme_dbname=MEME_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('meme_db', meme_dbname)



class MemeDb(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    resid = ndb.BlobKeyProperty()
    icon    = ndb.BlobProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    myid   = ndb.StringProperty()
    tags    = ndb.StringProperty(repeated=True)

class UserMemeDb(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    resid = ndb.StringProperty()
    blobid = ndb.BlobKeyProperty();
    date = ndb.DateTimeProperty(auto_now_add=True)
    userid   = ndb.IntegerProperty()
    shareid   = ndb.StringProperty()
    commentid = ndb.StringProperty()
    tags    = ndb.StringProperty(repeated=True)
    bid = ndb.StringProperty()

class SkelUploadHandler(blobstore_handlers.BlobstoreUploadHandler, AuthHandler):
  def post(self):
    upload_files = self.get_uploads('content')  # 'file' is file upload field in the form
    tags          = self.request.get('tags')
    blob_info = upload_files[0]
    meme = MemeDb(parent=meme_dbkey(MEME_DB_NAME))

    meme.resid = blob_info.key()
    meme.myid = str(meme.resid)
    meme.tags = tags.split(",")
    meme.put()

    self.response.write ("")

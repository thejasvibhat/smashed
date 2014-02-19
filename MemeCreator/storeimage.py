import webapp2
import urllib
import re,base64
from google.appengine.ext import ndb
from google.appengine.api import files
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
    userid   = ndb.IntegerProperty()
    mode = ndb.StringProperty()

class UserMemeDb(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    resid = ndb.StringProperty()
    blobid = ndb.BlobKeyProperty();
    date = ndb.DateTimeProperty(auto_now_add=True)
    userid   = ndb.IntegerProperty()
    shareid   = ndb.StringProperty()
    commentid = ndb.StringProperty()
    tags    = ndb.StringProperty(repeated=True)
    mode = ndb.StringProperty()
    bid = ndb.StringProperty()

class SkelUploadHandler(blobstore_handlers.BlobstoreUploadHandler, AuthHandler):
  def post(self):
    upload_files = self.get_uploads('content')  # 'file' is file upload field in the form
    tags         = self.request.get('tags')
    mode  = self.request.get('pmode', default_value="public")
    blob_info = upload_files[0]
    meme = MemeDb(parent=meme_dbkey(MEME_DB_NAME))
    meme.userid = self.user_id
    meme.resid = blob_info.key()
    meme.myid = str(meme.resid)
    meme.tags = tags.split(",")
    meme.mode = mode
    meme.put()

    self.response.write ("")

class SkelMobileUploadHandler(blobstore_handlers.BlobstoreUploadHandler, AuthHandler):
  def post(self):
    mode  = self.request.get('pmode', default_value="public")
    tags  = self.request.get('tags', default_value="Smashed")
    try:
      data = self.request.get('imgdata')
      data_to_64 = data
      decoded = data_to_64.decode('base64')

      # Create the file
      file_name = files.blobstore.create(mime_type='image/png')

      # Open the file and write to it
      with files.open(file_name, 'a') as f:
        f.write(decoded)          

      # Finalize the file. Do this before attempting to read it.
      files.finalize(file_name)

      key = files.blobstore.get_blob_key(file_name)
      meme = MemeDb(parent=meme_dbkey(MEME_DB_NAME))
      meme.userid = self.user_id
      meme.resid = key
      meme.myid = str(meme.resid)
      meme.tags = tags.split(",")
      meme.mode = mode
      meme.put()

      self.response.write ("")

    except Exception, e:      
      print e


import webapp2
import urllib

from google.appengine.ext import ndb

from google.appengine.api import images

from google.appengine.ext import db

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from User.handlers import AuthHandler

MEME_DB_NAME = 'meme_db'

MAIN_PAGE_FOOTER_TEMPLATE = """\
<head>
<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
    <script src="http://cdn.jquerytools.org/1.2.7/full/jquery.tools.min.js"></script>
  <!--script src="http://code.jquery.com/jquery-1.9.1.js"></script!-->
  <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
  <script  src="./assets/meme.js"></script>
  </head>
    <form action="%s" method="POST" enctype="multipart/form-data">
      <input name="content" type="file" />
      <div><input type="submit" value="Store Meme"></div>
    </form>
    <input type="file" id="myFile" style="display:none;">
</html>
"""


def meme_dbkey(meme_dbname=MEME_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('meme_db', meme_dbname)



class MemeDb(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    resid = ndb.BlobKeyProperty()
    icon    = ndb.BlobProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    myid   = ndb.StringProperty()

class UserMemeDb(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    resid = ndb.StringProperty()
    blobid = ndb.BlobKeyProperty();
    date = ndb.DateTimeProperty(auto_now_add=True)
    userid   = ndb.IntegerProperty()
    shareid   = ndb.StringProperty()

    '''
class MainPageStore(AuthHandler):

    def get(self):
        upload_url = blobstore.create_upload_url('/meme/store/upload')
        self.response.write('<html><body>')
        meme_query = MemeDb.query(ancestor=meme_dbkey(MEME_DB_NAME)).order(-MemeDb.date)
        memes = meme_query.fetch(10)

        for meme in memes:
            query_params = {'id': meme.myid}                
            self.response.write('<img src="/download/meme/icon?' + urllib.urlencode(query_params) + '"/>')

            # Write the submission form and the footer of the page
        #sign_query_params = urllib.urlencode({'meme_db': MEME_DB_NAME})
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE %
                            (upload_url))
'''

class SkelUploadHandler(blobstore_handlers.BlobstoreUploadHandler, AuthHandler):
  def post(self):
    upload_files = self.get_uploads('content')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    meme = MemeDb(parent=meme_dbkey(MEME_DB_NAME))

    meme.resid = blob_info.key()
    meme.myid = str(meme.resid)
    blob_key = meme.resid
    img = images.Image(blob_key=blob_key)
    img.resize(width=200, height=200)
    img.im_feeling_lucky()
    thumbnail = img.execute_transforms(output_encoding=images.JPEG)
    meme.icon = db.Blob(thumbnail)
    meme.put()

    self.response.write ("")

# application = webapp2.WSGIApplication([
#     ('/meme/store/storeview', MainPageStore),
#     ('/meme/store/upload', UploadHandler),    
# #    ('/actions/serve/([^/]+)?', ServeHandler)
# ], debug=True)

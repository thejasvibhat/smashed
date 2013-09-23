import webapp2

import cgi
import urllib

from google.appengine.api import users

from google.appengine.ext import ndb

from google.appengine.api import images

from PIL import Image, ImageDraw, ImageFont

import StringIO

from google.appengine.ext import db

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from google.appengine.api import memcache

from google.appengine.api import files

import xml.etree.ElementTree as ET

import textwrap

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

		
class MainPageStore(webapp2.RequestHandler):

    def get(self):
        upload_url = blobstore.create_upload_url('/actions/upload')
        self.response.write('<html><body>')
        meme_query = MemeDb.query(ancestor=meme_dbkey(MEME_DB_NAME)).order(-MemeDb.date)
        memes = meme_query.fetch(10)

        for meme in memes:
            query_params = {'id': meme.myid}				
            self.response.write('<img src="/download/icon?' + urllib.urlencode(query_params) + '"/>')

			# Write the submission form and the footer of the page
        #sign_query_params = urllib.urlencode({'meme_db': MEME_DB_NAME})
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE %
                            (upload_url))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
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

    self.redirect('/actions/storeview')


class ListFiles(webapp2.RequestHandler):

    def get(self):
        meme_query = MemeDb.query(ancestor=meme_dbkey(MEME_DB_NAME)).order(-MemeDb.date)
        memes = meme_query.fetch(10)

        self.response.write('<head>')
        for meme in memes:
            self.response.write('<url>')
            self.response.write('/download/icon?id=%s' %
                                meme.myid)
            self.response.write('</url>')
        self.response.write('</head>')



class GetFile(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self):
        myId=self.request.get('id')
        
        meme_dbname = self.request.get('meme_db',MEME_DB_NAME)
        meme_query = MemeDb.query(ancestor=meme_dbkey(meme_dbname)).order(-MemeDb.date)
        memes = meme_query.fetch(10)


        for meme in memes:
            if meme.myid == myId:
                    blob_info = blobstore.BlobInfo.get(meme.resid)
                    self.send_blob(blob_info)

class GetIcon(webapp2.RequestHandler):

    def get(self):
        myId=self.request.get('id')
        
        meme_dbname = self.request.get('meme_db',MEME_DB_NAME)
        meme_query = MemeDb.query(ancestor=meme_dbkey(meme_dbname)).order(-MemeDb.date)
        memes = meme_query.fetch(10)


        for meme in memes:
            if meme.myid == myId:
                self.response.write('%s' %
                                meme.icon)
              
class SaveHandler(webapp2.RequestHandler):
    def post(self):
        root = ET.fromstring(self.request.get('data'))
        imgId = ''
        family = ''
        size = ''
        color = ''
        style = ''
        weight = ''
        
        for objects in root:
            selectionx = objects.get('x')
            selectiony = objects.get('y')
            selectionwidth = objects.get('width')
            selectionheight = objects.get('height')
            for texts in objects:                
                if texts.tag == "{http://www.w3.org/1999/xhtml}img":                    
                    imgId = texts.get('id')
                    imgwidth = texts.get('width')
                    imgheight = texts.get('height')
                for child in texts.iter('{http://www.w3.org/1999/xhtml}text'):
                    for props in child:
                        family = props.get('name')
                        color = props.get('color')
                        size = props.get('size')
                        style = props.get('style')
                        weight = props.get('weight')
                        top = props.get('top')
                        left = props.get('left')
                        width = props.get('width')
                        height = props.get('height')
                        textVal = props.get('textVal')
                        
# create new image
        back_layer = Image.new('RGBA', (450,450), (100, 0, 0, 100))
        text_img = Image.new('RGBA', (int(width),int(height)), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)
        draw.text((0, 0), textVal, font=ImageFont.truetype(GetFontName(family,style,weight),int(size)),fill=color)

        # no write access on GAE
        output = StringIO.StringIO()
        text_img.save(output, format="png")
        text_layer = output.getvalue()
        output.close()
        output = StringIO.StringIO()
        back_layer.save(output, format="png")
        back_layer = output.getvalue()
        output.close()
        # read background image
        meme_query = MemeDb.query(ancestor=meme_dbkey(MEME_DB_NAME)).order(-MemeDb.date)
        memes = meme_query.fetch(10)
        for meme in memes:
            if meme.myid == imgId:
                blob_reader = blobstore.BlobReader(meme.resid)
                background = images.Image(blob_reader.read())

                background.resize(width=int(imgwidth), height=int(imgheight))
                background.im_feeling_lucky()
                thumbnail = background.execute_transforms(output_encoding=images.JPEG)
                # merge
                merged = images.composite([(thumbnail, (450-int(imgwidth))/2, (450 - int(imgheight))/2, 1.0, images.TOP_LEFT), 
                                           (text_layer,  int(float(left)),int(float(top)), 1.0, images.TOP_LEFT)], 
                                           450, 450)

                merged = images.composite([(back_layer, 0, 0, 1.0, images.TOP_LEFT), 
                                           (merged, 0, 0, 1.0, images.TOP_LEFT)], 
                                           450, 450)

                #merged = images.crop(merged,float(selectionx),float(selectiony),float(selectionwidth),float(selectionheight))
                merged = images.crop(merged,float(selectionx),float(selectiony),float(selectionwidth),float(selectionheight))
                
                # save
                file_name = files.blobstore.create(mime_type='image/png')
                with files.open(file_name, 'a') as f:
                    f.write(merged)
                files.finalize(file_name)
                self.redirect('/actions/storeview')
        

    
def GetFontName(oFamily,oStyle,oWeight):
    
    if oFamily == "Arial":
        name = 'fonts/arial'
    elif oFamily == "Verdana":
        name = 'fonts/verdana'
    elif oFamily == "Times":
        name = 'fonts/times'
    elif oFamily == "Trebucet":
        name = 'fonts/trebuc'
        
    if oWeight == "Bold":
        if oStyle == "Italic":
            name = name+'bi.ttf'
        else:
            name = name+'b.ttf'
    else:
        if oStyle == "Italic":
            name = name+'i.ttf'
        else:
            name = name+'.ttf'
    return name
            
            
        
        
       
    
application = webapp2.WSGIApplication([
    ('/actions/storeview', MainPageStore),
    ('/actions/list',ListFiles),
    ('/download/icon',GetIcon),
    ('/download/file',GetFile),
    ('/actions/upload', UploadHandler),
    ('/actions/save', SaveHandler),
    
#    ('/actions/serve/([^/]+)?', ServeHandler)
], debug=True)

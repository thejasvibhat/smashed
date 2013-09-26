import webapp2
import urllib
from google.appengine.ext import ndb

from google.appengine.api import images

from PIL import Image, ImageDraw, ImageFont

import StringIO

from google.appengine.ext import db

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


from google.appengine.api import files

import xml.etree.ElementTree as ET

from MemeCreator.storeimage import MemeDb


MEME_DB_NAME = 'meme_db'

def meme_dbkey(meme_dbname=MEME_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('meme_db', meme_dbname)

class ListFiles(webapp2.RequestHandler):

    def get(self):
        meme_query = MemeDb.query(ancestor=meme_dbkey(MEME_DB_NAME)).order(-MemeDb.date)
        memes = meme_query.fetch(10)

        self.response.write('<head>')
        for meme in memes:
            self.response.write('<url>')
            self.response.write('/download/meme/icon?id=%s' %
                                meme.myid)
            self.response.write('</url>')
        self.response.write('</head>')
              
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
                self.redirect('/meme/index.html')
        

    
def GetFontName(oFamily,oStyle,oWeight):
    
    if oFamily == "Arial":
        name = 'MemeCreator/fonts/arial'
    elif oFamily == "Verdana":
        name = 'MemeCreator/fonts/verdana'
    elif oFamily == "Times":
        name = 'fonts/times'
    elif oFamily == "Trebucet":
        name = 'MemeCreator/fonts/trebuc'
        
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
    ('/meme/actions/list',ListFiles),
    ('/meme/actions/save', SaveHandler),
    
#    ('/actions/serve/([^/]+)?', ServeHandler)
], debug=True)

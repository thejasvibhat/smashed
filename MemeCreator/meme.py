import webapp2
import math
import urllib
import os
import json
from facepy import GraphAPI
from google.appengine.ext import ndb
import uuid
from google.appengine.api import images
import logging
from PIL import Image, ImageDraw, ImageFont
from google.appengine.api import urlfetch
import StringIO
import textwrap
from google.appengine.ext import db

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from webapp2_extras import auth, sessions

from google.appengine.api import files

import xml.etree.ElementTree as ET

from MemeCreator.storeimage import MemeDb
from MemeCreator.storeimage import UserMemeDb
from User.handlers import AuthHandler
from Cheetah.Template import Template
from skel.skel import Skel
from MemeCreator.comments import *
MEME_DB_NAME = 'meme_db'

USER_MEME_DB_NAME = 'user_meme_db'

def meme_dbkey(meme_dbname=MEME_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('meme_db', meme_dbname)

def user_meme_dbkey(meme_userdbname=USER_MEME_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('user_meme_db', meme_userdbname)

def SaveFinalMeme(userid,file_name,tags):
    usermeme = UserMemeDb(parent=user_meme_dbkey(USER_MEME_DB_NAME))
    usermeme.resid = str(uuid.uuid4()) 
    usermeme.blobid = file_name
    usermeme.userid = userid
    usermeme.shareid = ''
    usermeme.tags = tags
    usermeme.commentid = CreateComment({}, 'init', userid)
    usermeme.put();
    return usermeme.resid;

def UpdateFacebookId(resid,postid):
    meme_query = UserMemeDb.query(UserMemeDb.resid == resid)
    memes = meme_query.fetch(1)
    for meme in memes:
        meme.shareid = postid
        meme.put();
	
class ListMeme(webapp2.RequestHandler):
    def get(self):
        tag = self.request.get('tag',default_value="auto")        
        if tag == "auto":
            meme_query = UserMemeDb.query(ancestor=user_meme_dbkey(USER_MEME_DB_NAME)).order(-UserMemeDb.date)
        else:
            meme_query = UserMemeDb.query(UserMemeDb.tags == tag).order(-UserMemeDb.date)
        
        oLimit = int(self.request.get("limit"))
        oOffset = int(self.request.get("offset"))
        memes = meme_query.fetch(oLimit,offset=oOffset)
        self.response.write('<memes>')
        for meme in memes:
            l_auth = auth.get_auth()
            userData = l_auth.store.user_model.get_by_id (meme.userid)
            #logging.info(userData)
            self.response.write('<meme>')
            self.response.write('<ts>')
            self.response.write('%s' %meme.date)
            self.response.write('</ts>')			
            self.response.write('<icon>')
            self.response.write('/res/icon/%s' %meme.blobid)
            self.response.write('</icon>')
            self.response.write('<url>')
            self.response.write('/oh/%s' %meme.resid)
            self.response.write('</url>')
            
            self.response.write('<creatorname>')
            self.response.write('%s' %userData.name)
            self.response.write('</creatorname>')

            self.response.write('<creatoravatar>')
            self.response.write('%s' %userData.avatar_url)
            self.response.write('</creatoravatar>')

            self.response.write('</meme>')
        self.response.write('</memes>')
            
class GetMeme(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resid = resource
        meme_query = UserMemeDb.query(UserMemeDb.resid == resid)
        memes = meme_query.fetch(1)
        for meme in memes:
            blob_info = blobstore.BlobInfo.get(meme.blobid)
            self.send_blob(blob_info)

class GetOh (AuthHandler):
    def get(self, resource):
        resid = resource 
	l_skel = Skel()
	l_skel.title = "Smashed.in :: OverHeards"

        meme_query = UserMemeDb.query(UserMemeDb.resid == resid)
        memes = meme_query.fetch(1)
        meme = memes[0]
        template_values = {
            'memeurl':   '/res/download/%s' % meme.blobid,
            'conturl':   '/oh/%s' % meme.resid,
            'shareid':   '%s' % meme.shareid,
            'currentid': '%s' % meme.resid,
            'commentid': '%s' % meme.commentid
            }

	#Head
	head_path = os.path.join (os.path.dirname(__file__), 'templates/ohview-head.tmpl')
	l_skel.addtohead(str((Template.compile(file=head_path)(searchList=template_values))))

	#body
        path = os.path.join (os.path.dirname (__file__), 'templates/ohview-body.tmpl')
	l_skel.addtobody (str((Template.compile(file=path)(searchList=template_values))))

        self.response.out.write(l_skel.gethtml())

class GetOhList (AuthHandler):
    def get(self, pagenum=1):
        pagenum = int(pagenum)
        l_skel = Skel()
        l_skel.title = "Smashed.in :: OverHeards"
        items_per_page = 10
        offset = 0
        if pagenum != 1:
            offset = (pagenum * items_per_page) - 1

        #Head
        head_path = os.path.join (os.path.dirname(__file__), 'templates/oh-head.tmpl')
        l_skel.addtohead(str((Template.compile(file=head_path)(searchList={}))))

        #body
        path = os.path.join (os.path.dirname (__file__), 'templates/oh-body.tmpl')
        meme_query = UserMemeDb.query(ancestor=user_meme_dbkey(USER_MEME_DB_NAME)).order(-UserMemeDb.date)
        memes = meme_query.fetch()
        totalCount = len(memes)

        template_values = {
            "memes" : memes[offset:offset+items_per_page],
            "currentpage" : pagenum,
            "totalpagecount" : math.ceil(totalCount / items_per_page)
            }

        l_skel.addtobody (str((Template.compile(file=path)(searchList=template_values))))

        self.response.out.write(l_skel.gethtml())	   
        
class ListCommentsOh(AuthHandler):
    def get (self):
        resource = self.request.get ("commentid");
        userDetails = self.current_user
        commentid = resource
        usercomments_querry = CommentDb.query(CommentDb.parentid == commentid).order(-CommentDb.date)
        oLimit = int(self.request.get("limit", default_value="10"))
        oOffset = int(self.request.get("offset", default_value="0"))
        usercomments = usercomments_querry.fetch(oLimit,offset=oOffset)
        finalDict = {}
        finalDict['currentuser'] = '%s' %userDetails.name
        finalDict['currentavatar'] = '%s' %userDetails.avatar_url
        allCommentsDict = []
        for usercomment in usercomments:
            l_auth = auth.get_auth()
            userData = l_auth.store.user_model.get_by_id(usercomment.userid)
            commentsDict = {}
            commentsDict['comment'] = usercomment.comment
            commentsDict['commentid'] = usercomment.commentid
            commentsDict['username'] = userData.name
            commentsDict['avatar'] = userData.avatar_url
            allCommentsDict.append(commentsDict)
        finalDict['comments'] = allCommentsDict
        self.response.write(json.dumps(finalDict))	
        
class UploadFacebook(AuthHandler):
    def get(self, resource):
        splitres = resource.split(':') 
        resid = splitres[0]		
        shareid = splitres[1]		
        meme_query = UserMemeDb.query(UserMemeDb.resid == resid)
        memes = meme_query.fetch(1)
        for meme in memes:
			meme.shareid = shareid
			meme.put()
        self.response.write('%s' %shareid)

class SkelList (webapp2.RequestHandler):
    def get(self):

        tag = self.request.get('tag',default_value="auto")        
        if tag == "auto":
            meme_query = MemeDb.query(ancestor=meme_dbkey(MEME_DB_NAME)).order(-MemeDb.date)
        else:
            meme_query = MemeDb.query(MemeDb.tags == tag).order(-MemeDb.date)
        memes = meme_query.fetch(10)        	

        #TODO: Make this valid XML or JSON
        self.response.write('<head>')
        for meme in memes:
            self.response.write('<url>')
            self.response.write('/res/icon/%s' % meme.resid)
            self.response.write('</url>')
        self.response.write('</head>')
              
class SaveHandler(AuthHandler):
    def post(self):
        userId = self.user_id
        root = ET.fromstring(self.request.get('data'))
        remove_namespace(root,"http://www.w3.org/1999/xhtml")
        imgId = ''
        family = ''
        size = ''
        color = ''
        style = ''
        weight = ''
        shadowcolor = "black"
        textlayers = []
        tags = []
        for objects in root:
            selectionx = objects.get('x')
            selectiony = objects.get('y')
            selectionwidth = objects.get('width')
            selectionheight = objects.get('height')
            for texts in objects:                
                if texts.tag == "imagebase":                    
                    imgId = texts.get('id')
                    imgwidth = texts.get('width')
                    imgheight = texts.get('height')
                            # read background image
                    meme_query =  MemeDb.query(MemeDb.myid == imgId)
                    #meme_query = MemeDb.query(ancestor=meme_dbkey(MEME_DB_NAME)).order(-MemeDb.date)
                    memes = meme_query.fetch(1)
                    for meme in memes:
                        blob_reader = blobstore.BlobReader(meme.resid)
                        background = images.Image(blob_reader.read())
                        tags = meme.tags
                        background.resize(width=int(imgwidth), height=int(imgheight))
                        background.im_feeling_lucky()
                        thumbnail = background.execute_transforms(output_encoding=images.JPEG)
                        back_layer = Image.new('RGBA', (550,550), (100, 0, 0, 100))
                        output = StringIO.StringIO()
                        back_layer.save(output, format="png")
                        back_layer = output.getvalue()
                        output.close()               
                        #merge
                        merged = images.composite([(back_layer, 0,0, 1.0, images.TOP_LEFT), 
                                                   (thumbnail, (550-int(imgwidth))/2, (550 - int(imgheight))/2, 1.0, images.TOP_LEFT)], 
                                                   550, 550)


                for child in texts.iter('text'):
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
                        text_img = Image.new('RGBA', (int(width),int(height)), (0, 0, 0, 0))
                        draw = ImageDraw.Draw(text_img)
                        font=ImageFont.truetype(GetFontName(family,style,weight),int(size))
                        #width, height1 = font.getsize(textVal)
                        apString = '' 
                        lines = []
                        for x in range(0, len(textVal)):
                            tempString = apString
                            apString = apString + '%s' %textVal[x]                            
                            width1, height1 = font.getsize(apString)
                            if width1 >= int(width):
                                lines.append(tempString)
                                apString = '%s' %textVal[x]
                        if apString != '':
                            lines.append(apString)
                        #lines = textwrap.wrap(textVal, width = 10)
                        y_text = 0
                        for line in lines:
                            font=ImageFont.truetype(GetFontName(family,style,weight),int(size))
                            width1, height1 = font.getsize(line)    
                            draw.text((-2, y_text-2), line, font=font, fill=shadowcolor)
                            draw.text((+2, y_text-2), line, font=font, fill=shadowcolor)
                            draw.text((-2, y_text+2), line, font=font, fill=shadowcolor)
                            draw.text((+2, y_text+2), line, font=font, fill=shadowcolor)
                            draw.text((0, y_text), line, font = font,fill=color)
                            y_text += height1
                        #draw.text((0, 0), textVal, font=ImageFont.truetype(GetFontName(family,style,weight),int(size)),fill=color)
                
                        # no write access on GAE
                        output = StringIO.StringIO()
                        text_img.save(output, format="png")
                        text_layer = output.getvalue()
                        output.close()
                        textlayers.append(text_layer)
                        merged = images.composite([(merged, 0,0, 1.0, images.TOP_LEFT), 
                                                   (text_layer,  int(float(left)),int(float(top)), 1.0, images.TOP_LEFT)], 
                                                   550, 550)

                        
        #merged = images.crop(merged,float(selectionx),float(selectiony),
        #                     float(selectionwidth),float(selectionheight))
        merged = images.crop(merged,float(selectionx),float(selectiony),
                             float(selectionwidth),float(selectionheight))
        
        # save
        file_name = files.blobstore.create(mime_type='image/png')
        with files.open(file_name, 'a') as f:
            f.write(merged)
        files.finalize(file_name)     
        blob_key = files.blobstore.get_blob_key(file_name)           
        memeid = SaveFinalMeme(userId,blob_key,tags)
        oauth_access_token = 'CAABvnvDx5ZAgBAKgqY3ci6hIlnKxaiOM9zEyc3AZAhbEc97JtEAhpUpTbwZAMONaScwq1xL2TgefulTFJ7FMRuKwIihLBwifzDX9sFfVxuytOwoVU1jPPDKPP13bvZBp7hin9aDjZCKfbKWFZCuRtOSPAcqgWUuC31CvFeXDpuzsvgKEguQ8ZCig7IWL1h8ElUZD&expires=5183863'
        graph = GraphAPI(oauth_access_token)

        # Get my latest posts
        # Post a photo of a parrot

        urlfetch.set_default_fetch_deadline(45)
        postid = graph.post(
                       path = '/10153430700220062/photos',
                       message = 'photo description',
                       url = 'http://smashed.thejasvi.in/res/download/%s' % blob_key
                       )
        #logging.info('theju/%s' % postid['id'])
        UpdateFacebookId (memeid,postid['id'])

        self.response.write ('%s' % memeid)
        #self.redirect('/meme/store/memeview/%s' %memeid)
        

    
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
            
            

def remove_namespace(doc, namespace):
    """Remove namespace in the passed document in place."""
    ns = u'{%s}' % namespace
    nsl = len(ns)
    for elem in doc.getiterator():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]

        
        
       
    
# application = webapp2.WSGIApplication([
#     ('/meme/actions/list',ListFiles),
#     ('/meme/actions/listmeme',ListMeme),
#     ('/meme/actions/getmeme/([^/]+)?',GetMeme),
#     ('/meme/actions/save', SaveHandler),
# #    ('/actions/serve/([^/]+)?', ServeHandler)
# ], debug=True)

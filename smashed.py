import os
import sys
sys.path.append (os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lib'))
#sys.path.append (os.path.join(os.path.abspath(os.path.dirname(__file__)), '.'))

import webapp2
import logging
#from webapp2_extras import auth, sessions, jinja2, users
from Cheetah.Template import Template

from User.handlers import AuthHandler
from secrets import secrets

from MemeCreator.creatememe import *

#from MemeCreator.storeimage import MainPageStore
from MemeCreator.storeimage import *

# from MemeCreator.meme import ListFiles
# from MemeCreator.meme import SaveHandler
# from MemeCreator.meme import ListMeme
# from MemeCreator.meme import GetMeme
# from MemeCreator.meme import GetShareMemeView
# from MemeCreator.meme import GetListMemeView
# from MemeCreator.meme import UploadFacebook

from MemeCreator.meme import *

import Barreviews.listreviews

from Barreviews.listreviews import ListScenesHandler
from Barreviews.listreviews import SearchHandler
from Barreviews.review import SceneHandler
from Barreviews.review import ReviewHandler
from Barreviews.listreviews import ListComments

from Barreviews.storereview import *

from Barreviews.comments import *
from DataDump.download import GetRes
from DataDump.download import GetIcon


class ComingSoon (AuthHandler):

    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates/comingsoon.tmpl')
        tclass = Template.compile (file = path)

        logging.info (self.logged_in)
        t = tclass(searchList=template_values)

        self.response.out.write(t)

# Map URLs to handlers
routes = [
  webapp2.Route ('/', handler=ComingSoon),

  webapp2.Route ('/oh', GetOhList),    #OH List (VIEW)
  webapp2.Route ('/oh/record', OhRecordHandler),    #oh creator (VIEW)
  webapp2.Route ('/oh/<resource>', GetOh),    #OH Single (VIEW)

  webapp2.Route ('/api/oh/skel-preupload', SkelPreUploadHandler), #OH lib/skel upload URL creator (API)
  webapp2.Route ('/api/oh/skel-upload', SkelUploadHandler),    #oh lib/skel upload (API)
  webapp2.Route ('/api/oh/skel-list', SkelList), #OH lib/skel list (API)

  webapp2.Route ('/api/oh/save', SaveHandler), #OH Save (API)
  webapp2.Route ('/api/oh/list', ListMeme), #OH List (API), Used for ticker


  webapp2.Route ('/b', ReviewHandler), #BR list (VIEW)
  webapp2.Route ('/b/record', BRecordHandler), #BR create/upload (VIEW)
  webapp2.Route ('/b/<resource>', SceneHandler), #BR Single (VIEW)
  webapp2.Route ('/b/<resource>/<name>', SceneHandler), #BR Single (VIEW)
 
  webapp2.Route ('/api/b/list', ListScenesHandler),
  webapp2.Route ('/api/b/comments', ListComments),
  webapp2.Route ('/api/b/updatecomment', AddComment),
  webapp2.Route ('/api/b/upload', BSaveHandler),
  
  # #Reviews/storereview.py
  #webapp2.Route ('/reviews/store/uploadreview', MainPageStore1), #BR create/upload (VIEW)
  #webapp2.Route ('/reviews/store/upload', UploadHandler1), #BR create/upload (API)


  # #DataDump.download.py
  # webapp2.Route ('/download/review/icon/<resource>', GetIconReview), #BR resource
  # webapp2.Route ('/download/review/file/<resource>', GetFileReview) #BR resource

  webapp2.Route ('/res/download/<resource>', GetRes), #OH res download (API/Path)
  webapp2.Route ('/res/icon/<resource>', GetIcon), #OH res download (API/Path)
]

# webapp2 config
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': secrets.SESSION_KEY
  },
  'webapp2_extras.auth': {
    'user_attributes': []
  }
}

application = webapp2.WSGIApplication (routes, config=app_config, debug=True)


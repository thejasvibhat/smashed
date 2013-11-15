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

from MemeCreator.storeimage import MainPageStore
from MemeCreator.storeimage import UploadHandler

from MemeCreator.meme import ListFiles
from MemeCreator.meme import SaveHandler
from MemeCreator.meme import ListMeme
from MemeCreator.meme import GetMeme
from MemeCreator.meme import GetShareMemeView

import Barreviews.listreviews
#logging.info ("%s" % Reviews)

from Barreviews.listreviews import ListScenesHandler
from Barreviews.listreviews import SearchHandler
from Barreviews.review import SceneHandler

from Barreviews.storereview import MainPageStore as MainPageStore1
from Barreviews.storereview import UploadHandler as UploadHandler1

from DataDump.download import GetIcon
from DataDump.download import GetFile
from DataDump.download import GetIconReview
from DataDump.download import GetFileReview


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

  #MemeCreator/storeimage.py
  webapp2.Route ('/meme/store/storeview', MainPageStore),
  webapp2.Route ('/meme/store/upload', UploadHandler),    
  webapp2.Route ('/meme/store/create', CreateMemeHandler),    
  webapp2.Route ('/meme/store/uploadskeleton', UploadMemeHandler),
  webapp2.Route ('/meme/store/memeview/<resource>', GetShareMemeView),

  #MemeCreator/meme.py
  webapp2.Route ('/meme/actions/list', ListFiles),
  webapp2.Route ('/meme/actions/save', SaveHandler),
  webapp2.Route ('/meme/actions/listmeme', ListMeme),
  webapp2.Route ('/meme/actions/getmeme/<resource>', GetMeme),

  # #Reviews/review.py
  webapp2.Route ('/reviews/scenes/listscenes', ListScenesHandler),
  webapp2.Route ('/reviews/scenes/search', SearchHandler),
  webapp2.Route ('/reviews/scenes/<resource>', SceneHandler),    

  # #Reviews/storereview.py
  webapp2.Route ('/reviews/store/uploadreview', MainPageStore1),
  webapp2.Route ('/reviews/store/upload', UploadHandler1),
  
  # #DataDump.download.py
  webapp2.Route ('/download/meme/icon', GetIcon),
  webapp2.Route ('/download/meme/file', GetFile),
  webapp2.Route ('/download/review/icon/<resource>', GetIconReview),
  webapp2.Route ('/download/review/file/<resource>', GetFileReview)

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


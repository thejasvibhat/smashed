import os
import sys
sys.path.append (os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lib'))
#sys.path.append (os.path.join(os.path.abspath(os.path.dirname(__file__)), '.'))

import webapp2
import logging
#from webapp2_extras import auth, sessions, jinja2, users
from webapp2_extras import routes
from Cheetah.Template import Template

from User.handlers import AuthHandler
from User.user import User
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
from MemeCreator.comments import *
import Barreviews.listreviews

from Barreviews.listreviews import ListScenesHandler
from Barreviews.listreviews import SearchHandler
from Barreviews.review import SceneHandler
from Barreviews.review import ReviewHandler
from Barreviews.listreviews import ListComments
from Barreviews.listreviews import AjaxLocality

from Barreviews.storereview import *

from Barreviews.comments import *
from Barreviews.delete import *
from DataDump.download import GetRes
from DataDump.download import GetIcon

from landing.landing import LandingPage
from checktoken import *
from scrapper import *

from SitePages.sitepages import *

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
  webapp2.Route ('/', handler=LandingPage),

  routes.RedirectRoute ('/oh', handler=GetOhList, name = "oh", strict_slash=True),
  routes.RedirectRoute ('/oh/page/<pagenum>', handler=GetOhList, name = "ohpage", strict_slash=True), 
  webapp2.Route ('/oh/record', OhRecordHandler),    #oh creator (VIEW)
  webapp2.Route ('/oh/<resource>', GetOh),    #OH Single (VIEW)

  webapp2.Route ('/api/oh/skel-preupload', SkelPreUploadHandler), #OH lib/skel upload URL creator (API)
  webapp2.Route ('/api/oh/skel-upload', SkelUploadHandler),    #oh lib/skel upload (API)
  webapp2.Route ('/api/oh/skel-list', SkelList), #OH lib/skel list (API)
  webapp2.Route ('/api/oh/comments', ListCommentsOh),
  webapp2.Route ('/api/oh/updatecomment', AddCommentOh),

  webapp2.Route ('/api/oh/save', SaveHandler), #OH Save (API)
  webapp2.Route ('/api/oh/list', ListMeme), #OH List (API), Used for ticker


  routes.RedirectRoute ('/b', handler=ReviewHandler, name = "b", strict_slash=True),
  routes.RedirectRoute ('/b/page/<pagenum>', handler=ReviewHandler, name = "bpage", strict_slash=True),
  webapp2.Route ('/b/record', BRecordHandler), #BR create/upload (VIEW)
  webapp2.Route ('/b/edit/<resource>', BEditHandler), #BR create/upload (VIEW)
  webapp2.Route ('/b/<resource>', SceneHandler), #BR Single (VIEW)
  webapp2.Route ('/b/<resource>/<name>', SceneHandler), #BR Single (VIEW)
  
  webapp2.Route ('/pages/privacy', PrivacyHandler), #SitePages
  webapp2.Route ('/pages/about', AboutHandler), #SitePages
  webapp2.Route ('/pages/terms', TermsHandler), #SitePages
 
  webapp2.Route ('/api/b/list', ListScenesHandler),
  webapp2.Route ('/api/b/comments', ListComments),
  webapp2.Route ('/api/b/updatecomment', AddComment),
  webapp2.Route ('/api/b/updateusercomment', UpdateComment),
  webapp2.Route ('/api/b/upload', BSaveHandler),
  webapp2.Route ('/api/b/update', BSaveUpdateHandler),
  webapp2.Route ('/api/b/ajaxlist', AjaxLocality),
  webapp2.Route ('/api/b/delete', BDeleteHandler),
  
  # #Reviews/storereview.py
  #webapp2.Route ('/reviews/store/uploadreview', MainPageStore1), #BR create/upload (VIEW)
  #webapp2.Route ('/reviews/store/upload', UploadHandler1), #BR create/upload (API)


  # #DataDump.download.py
  # webapp2.Route ('/download/review/icon/<resource>', GetIconReview), #BR resource
  # webapp2.Route ('/download/review/file/<resource>', GetFileReview) #BR resource

  webapp2.Route ('/res/download/<resource>', GetRes), #OH res download (API/Path)
  webapp2.Route ('/res/icon/<resource>', GetIcon), #OH res download (API/Path)
  webapp2.Route ('/gettoken', BaseRequestHandler), 
  webapp2.Route ('/storelocality', PushLocality), 
]

# webapp2 config
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': secrets.SESSION_KEY
  },
  'webapp2_extras.auth': {
    'user_attributes': [],
    'user_model' : User
  }
}

def handle_404 (request, response, exception):
    logging.exception (exception)
    response.write ('Oops! I could swear this page was here!')
    response.set_status (404)

def handle_500 (request, response, exception):
    logging.exception (exception)
    response.write ('A server error occurred!')
    response.set_status (500)

application = webapp2.WSGIApplication (routes, config=app_config, debug=True)

application.error_handlers[500] = handle_500
application.error_handlers[404] = handle_404


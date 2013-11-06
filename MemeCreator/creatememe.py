import os
import logging
from google.appengine.ext import blobstore
from User.handlers import AuthHandler
from Cheetah.Template import Template

class CreateMemeHandler(AuthHandler):
    def get(self):        
        template_values = {}
        path = os.path.join(os.path.dirname(__file__),'views/creatememe.tmpl')
        tclass = Template.compile (file = path)
        t = tclass(searchList=template_values)
        logging.info (self.logged_in)
        self.response.out.write(t)

class UploadMemeHandler(AuthHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/meme/store/upload')
        self.response.write(upload_url)
        
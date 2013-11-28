import os
import logging
from google.appengine.ext import blobstore
from User.handlers import AuthHandler
from Cheetah.Template import Template

class OhRecordHandler (AuthHandler):
    def get(self):  
        if not self.logged_in:
            self.session['redirect_url'] = '/oh/record'
            self.redirect('/auth/')
        else:
            template_values = {}
            path = os.path.join(os.path.dirname(__file__),'views/creatememe.tmpl')
            tclass = Template.compile (file = path)
            t = tclass(searchList=template_values)
            logging.info (self.logged_in)
            self.response.out.write(t)

class SkelPreUploadHandler(AuthHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/api/oh/skel-upload')
        self.response.write(upload_url)
        

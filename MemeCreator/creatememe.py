import os
import logging
from google.appengine.ext import blobstore
from User.handlers import AuthHandler
from Cheetah.Template import Template
from skel.skel import Skel

class OhRecordHandler (AuthHandler):
    def get(self):  
        if not self.logged_in:
            self.session['redirect_url'] = '/oh/record'
            self.redirect('/auth/')
        else:
            l_skel = Skel()
            l_skel.title = "Smashed.in :: Record Your Overheard"

            #Head
            head_path = os.path.join (os.path.dirname (__file__), 'templates/createoh-head.tmpl')
            l_skel.addtohead (str((Template.compile(file=head_path) (searchList={}))))

            #Body
            template_values = {}
            path = os.path.join (os.path.dirname (__file__), 'templates/createoh-body.tmpl')
            l_skel.addtobody (str((Template.compile(file=path) (searchList=template_values))))

            self.response.out.write(l_skel.gethtml())

class SkelPreUploadHandler(AuthHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/api/oh/skel-upload')
        self.response.write(upload_url)
        

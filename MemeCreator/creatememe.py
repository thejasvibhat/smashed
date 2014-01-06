import os
import logging
from google.appengine.ext import blobstore
from User.handlers import AuthHandler
from Cheetah.Template import Template
from skel.skel import Skel

class OhRecordHandler (AuthHandler):
    def get(self):
        self.user_gatekeeper ()
        l_skel = Skel()
        l_skel.title = "Smashed.in :: Record Your Overheard"

        #Head
        head_path = os.path.join (os.path.dirname (__file__), 'templates/createoh-head-meta.tmpl')
        l_skel.addtohead (str((Template.compile(file=head_path) (searchList={}))))

        #Head
        head_path = os.path.join (os.path.dirname (__file__), 'templates/createoh-head.tmpl')
        l_skel.addtohead (str((Template.compile(file=head_path) (searchList={}))))

        #Body
        template_values = {}
        path = os.path.join (os.path.dirname (__file__), 'templates/createoh-body.tmpl')
        l_skel.addtobody (str((Template.compile(file=path) (searchList=template_values))))

        self.response.out.write(l_skel.gethtml())

class OhRecordBarHandler (AuthHandler):
    def get(self):
        self.user_gatekeeper ()
        data = []
#Head
        data.append('<div id="oh" title="Record Overheard" style="width:1080px;" >')
        data.append('<div>')
        head_path = os.path.join (os.path.dirname (__file__), 'templates/createoh-head.tmpl')
        data.append (str((Template.compile(file=head_path) (searchList={}))))

        #Body
        template_values = {}
        path = os.path.join (os.path.dirname (__file__), 'templates/createoh-body.tmpl')
        data.append (str((Template.compile(file=path) (searchList=template_values))))
        data.append('</div>')
        data.append('</div>')
        self.response.out.write("\n".join (data))
        
class SkelPreUploadHandler(AuthHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/api/oh/skel-upload')
        self.response.write(upload_url)
        

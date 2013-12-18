import webapp2
import sys
import os
import logging
from webapp2_extras import auth, sessions
from User.handlers import AuthHandler
sys.path.append (os.path.join(os.path.abspath(os.path.dirname(__file__)), '../lib'))

from Cheetah.Template import Template

from skel.skel import Skel


class PrivacyHandler(webapp2.RequestHandler):
    def get(self):
        l_skel = Skel()
	l_skel.title = "Smashed.in :: Privacy"
        #Head
        head_path = os.path.join (os.path.dirname (__file__), 'templates/privacy-head.tmpl')
        l_skel.addtohead (str((Template.compile(file=head_path) (searchList={}))))

        #Body
        path = os.path.join (os.path.dirname (__file__), 'templates/privacy-body.tmpl')
        l_skel.addtobody (str((Template.compile(file=path) (searchList={}))))

        self.response.out.write(l_skel.gethtml())

class TermsHandler(webapp2.RequestHandler):
    def get(self):
        l_skel = Skel()
        l_skel.title = "Smashed.in :: Terms of Use"
        #Head
        head_path = os.path.join (os.path.dirname (__file__), 'templates/terms-head.tmpl')
        l_skel.addtohead (str((Template.compile(file=head_path) (searchList={}))))

        #Body
        path = os.path.join (os.path.dirname (__file__), 'templates/terms-body.tmpl')
        l_skel.addtobody (str((Template.compile(file=path) (searchList={}))))

        self.response.out.write(l_skel.gethtml())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        l_skel = Skel()
        l_skel.title = "Smashed.in :: About Us"
        #Head
        head_path = os.path.join (os.path.dirname (__file__), 'templates/about-head.tmpl')
        l_skel.addtohead (str((Template.compile(file=head_path) (searchList={}))))

        #Body
        path = os.path.join (os.path.dirname (__file__), 'templates/about-body.tmpl')
        l_skel.addtobody (str((Template.compile(file=path) (searchList={}))))

        self.response.out.write(l_skel.gethtml())



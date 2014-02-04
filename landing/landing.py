import logging
import os

from User.handlers import AuthHandler
from Cheetah.Template import Template

from skel.skel import Skel

from inspect import ismethod
from User.user import User

def call_all(obj, *args, **kwargs):
    for name in dir(obj):
        attribute = getattr(obj, name)
        if callable(attribute):
            logging.info ("function: %s" % attribute)

class LandingPage (AuthHandler):
    def get(self):
        if self.logged_in:
            self.redirect('/b')
        else:
            l_skel = Skel()
            l_skel.title = "Smashed.In"

            #Head
            head_path = os.path.join (os.path.dirname (__file__), 'templates/landing-head.tmpl')
            l_skel.addtohead (str((Template.compile(file=head_path) (searchList={}))))

            path = os.path.join (os.path.dirname (__file__), 'templates/landing-body.tmpl')
            l_skel.addtobody (str((Template.compile(file=path) (searchList={}))))

            #logging.error ("SESSION digging %s" % self.session)
            #logging.error ("AUTH digging %s" % self.auth.get_session_data())

            self.response.out.write(l_skel.gethtml())

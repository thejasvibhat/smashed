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
        if not callable(attribute):
            logging.info ("function: %s" % attribute)

class LandingPage (AuthHandler):
    def get(self):
        l_skel = Skel()
        l_skel.title = "Smashed.In :: Stand n Deliver"

        #Head
        head_path = os.path.join (os.path.dirname (__file__), 'templates/landing-head.tmpl')
        l_skel.addtohead (str((Template.compile(file=head_path) (searchList={}))))

        path = os.path.join (os.path.dirname (__file__), 'templates/landing-body.tmpl')
        l_skel.addtobody (str((Template.compile(file=path) (searchList={}))))

        if self.isloggedin:
            logging.info ("digging %s %s" % (self.user_id, self.user_name))

        self.response.out.write(l_skel.gethtml())


import os

from User.handlers import AuthHandler
from Cheetah.Template import Template

from skel.skel import Skel

class LandingPage (AuthHandler):
    def get(self):
        l_skel = Skel()
        l_skel.title = "Smashed.In :: Stand n Deliver"

        #Head
        head_path = os.path.join (os.path.dirname (__file__), 'templates/landing-head.tmpl')
        l_skel.addtohead (str((Template.compile(file=head_path) (searchList={}))))

        path = os.path.join (os.path.dirname (__file__), 'templates/landing-body.tmpl')
        l_skel.addtobody (str((Template.compile(file=path) (searchList={}))))

        self.response.out.write(l_skel.gethtml())

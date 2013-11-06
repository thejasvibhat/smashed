import webapp2
import os
import sys
import logging
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

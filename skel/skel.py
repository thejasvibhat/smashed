import pprint
import os
import sys
from webapp2_extras import auth, sessions

from User.handlers import AuthHandler
from Cheetah.Template import Template

class Skel (AuthHandler):
    def __init__ (self):
        self.title = ""
        self.morehead = []
        self.skelbody = []

    def addtohead (self, element):
        self.morehead.append (element)
        return len(self.morehead)

    def addtobody (self, element):
        self.skelbody.append (element)
        return len(self.skelbody)

    def gethtml (self):
        path = os.path.join(os.path.dirname(__file__), 'templates/skel.tmpl')
        tclass = Template.compile (file = path)

        template_values = {
            "title" : self.title,
            "logged_in": self.logged_in,
            "morehead" : "\n".join (self.morehead),
            "skelbody" : "\n".join (self.skelbody)
            }

        if (self.isloggedin):
            name = self.user_name if self.user_name else "myName"

            template_values.update ({
                "avatar" : self.user.avatar_url,
                "name"   : name
                })

        t = tclass (searchList=template_values)
        return t
    
        
if __name__ == "__main__":
    skel01 = Skel ()
    
    skel01.title = "Test"
    skel01.addtobody ("<p>Some New TAG</p>");
    skel01.addtobody ("<p>Some Newer TAG</p>");

    print skel01.gethtml()

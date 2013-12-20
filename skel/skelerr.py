import pprint
import os
import sys

from Cheetah.Template import Template

class SkelErr (object):
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
            "logged_in": False,
            "morehead" : "\n".join (self.morehead),
            "skelbody" : "\n".join (self.skelbody)
            }

        t = tclass (searchList=template_values)
        return t
        
if __name__ == "__main__":
    skel01 = Skel ()
    
    skel01.title = "Test"
    skel01.addtobody ("<p>Some New TAG</p>");
    skel01.addtobody ("<p>Some Newer TAG</p>");

    print skel01.gethtml()
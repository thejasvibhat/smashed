import webapp2
import sys, json, random, string
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import logging
from User.handlers import AuthHandler	
SERVER = 'gcm.googleapis.com'
PORT = 5235
USERNAME = "849208174002"
PASSWORD = "AIzaSyBNnXeISW8-KfETBKE-r0ASytx4WyC6NTk"

unacked_messages_quota = 1000
send_queue = []
def push_dbkey(push_dbname="push_db"):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('push_db', "push_db")

class GcmData(ndb.Model):
    bid    = ndb.StringProperty()
    regid = ndb.StringProperty(repeated=True)
    messages = ndb.StringProperty(repeated=True)
    usernames = ndb.StringProperty(repeated=True)
    atplaces = ndb.StringProperty(repeated=True)

class GcMStart(AuthHandler):
    def get(self):
        bid = self.request.get("bid")
        bname = self.request.get("bname")
        regid = self.request.get("regid")
        message = self.request.get("message")
        atplace = self.request.get("atplace")
        userDetails = self.current_user
        push_query = GcmData.query(GcmData.bid == bid)	
        pushes = push_query.fetch(1) 
        registration_ids = []
        for push in pushes:
            for regs in push.regid:
                if regs != regid:
                    registration_ids.append(regs)
            messages = push.messages
            usernames = push.usernames
            atplaces = push.atplaces
            if len(messages) > 20:
                del messages[-1]
                del usernames[-1]
                del atplaces[-1]
                messages.append(message)
                usernames.append(userDetails.name)
                atplaces.append(atplace)
                push.messages = messages
                push.usernames = usernames
                push.atplaces = atplaces
                push.put()
            else:
                push.messages.append(message)
                push.usernames.append(userDetails.name)
                push.atplaces.append(atplace)
                push.put()

        logging.info("%s" %registration_ids)

	Bodyfields = {
	      "data": {"live":message,"username":userDetails.name,"bid":bid,"bname":bname,"atplace":atplace},
	      "registration_ids": registration_ids
	     }
	result = urlfetch.fetch(url="https://android.googleapis.com/gcm/send",
		        payload=json.dumps(Bodyfields),
		        method=urlfetch.POST,
		        headers={'Content-Type': 'application/json','Authorization': 'key=AIzaSyBNnXeISW8-KfETBKE-r0ASytx4WyC6NTk'})
        self.response.out.write('Server response, status: ' + result.content )
  
class GcmRegister(webapp2.RequestHandler):
    def get(self):
        regid = self.request.get("regid");
        bid = self.request.get("bid")    
        push_query = GcmData.query(GcmData.bid == bid)	
        pushes = push_query.fetch(1) 
        exists = False; 
        bidexists = False;

        for push in pushes:
            bidexists = True
            for regs in push.regid:
                if regs == regid:                    
                    exists = True
            
        if exists == False:
            if bidexists == True:
                for push in pushes:
                    push.regid.append(regid)
                    push.put()
            else:
                pushdb = GcmData(parent=push_dbkey("push_db"))
                pushdb.regid.append(regid)
                pushdb.bid = bid
                pushdb.put()      
        finalDict = {}
        allmessages = []
        for push in pushes:
            i = 0
            for message in push.messages:
                messageDict = {}
                messageDict['message'] = message
                messageDict['username'] = push.usernames[i]
                messageDict['atplace'] = push.atplaces[i]
                i = i + 1
                allmessages.append(messageDict)
        finalDict['messages'] = allmessages
        self.response.write(json.dumps(finalDict))	        


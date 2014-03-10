import webapp2
import sys, json, random,xmpp, string
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

class GcMStart(AuthHandler):
    def get(self):
        bid = self.request.get("bid")
        regid = self.request.get("regid")
        message = self.request.get("message")
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
            if len(messages) > 10:
                messages.pop()
                usernames.pop()
                messages.append(message)
                usernames.append(userDetails.name)
                push.messages = messages
                push.usernames = usernames
                push.put()
            else:
                push.messages.append(message)
                push.usernames.append(userDetails.name)
                push.put()

        logging.info("%s" %registration_ids)

	Bodyfields = {
	      "data": {"live":message,"username":userDetails.name},
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
                i = i + 1
                allmessages.append(messageDict)
        finalDict['messages'] = allmessages
        self.response.write(json.dumps(finalDict))	        


import webapp2
import datetime
import calendar
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

class InstantMesg (ndb.Model):
    message = ndb.StringProperty(index=False)
    atplace = ndb.StringProperty(index=False)
    userid = ndb.IntegerProperty(index=False)
    timestamps = ndb.DateTimeProperty(index=False)

class GcmData(ndb.Model):
    bid  = ndb.StringProperty()
    instants = ndb.StructuredProperty (InstantMesg, repeated=True)

class GcMStart(AuthHandler):
    def get(self):
        bid = self.request.get("bid")
        bname = self.request.get("bname")
        regid = self.request.get("regid")
        message = self.request.get("message")
        atplace = self.request.get("atplace")
        timestamp = datetime.datetime.now()
        userid = self.user_id
        userDetails = self.current_user
        push_query = GcmData.query(GcmData.bid == bid)	
        pushes = push_query.fetch(1) 
        registration_ids = []
        for push in pushes:
            for regs in push.regid:
                if regs != regid:
                    registration_ids.append(regs)
                else:
                    exists = True
            if exists == False:
                push.regid.append(regid)
                push.put()

            messages = push.messages
            usernames = push.usernames
            atplaces = push.atplaces
            userids = push.userids
            timestamps = push.timestamps
            if len(messages) > 20:
                del messages[-1]
                del usernames[-1]
                del atplaces[-1]
                del userids[-1]
                del timestamps[-1]
                messages.append(message)
                usernames.append(userDetails.name)
                atplaces.append(atplace)
                userids.append(userid)
                timestamps.append(timestamp)
                push.messages = messages
                push.usernames = usernames
                push.atplaces = atplaces
                push.userids = userids
                push.timestamps = timestamps
                push.put()
            else:
                push.messages.append(message)
                push.usernames.append(userDetails.name)
                push.atplaces.append(atplace)
                push.userids.append(userid)
                push.timestamps.append(timestamp)
                push.put()
        secs = calendar.timegm(timestamp.timetuple())
        logging.info("%s" %registration_ids)

	Bodyfields = {
	      "data": {"live":message,"username":userDetails.name,"bid":bid,"bname":bname,"atplace":atplace,"timestamp":secs},
	      "registration_ids": registration_ids
	     }
	result = urlfetch.fetch(url="https://android.googleapis.com/gcm/send",
		        payload=json.dumps(Bodyfields),
		        method=urlfetch.POST,
		        headers={'Content-Type': 'application/json','Authorization': 'key=AIzaSyBNnXeISW8-KfETBKE-r0ASytx4WyC6NTk'})
        self.response.out.write('Server response, status: ' + result.content )
  
class GcmRegister(AuthHandler):
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
                secs = calendar.timegm(push.timestamps[i].timetuple())
                messageDict['timestamp'] = secs
                if push.userids[i] == self.user_id:
                    messageDict['self'] = 'true'
                else:
                    messageDict['self'] = 'false'
                i = i + 1
                allmessages.append(messageDict)
        finalDict['messages'] = allmessages
        self.response.write(json.dumps(finalDict))	        


import webapp2
import uuid
import datetime
import calendar
import sys, json, random, string
from google.appengine.api import urlfetch
from webapp2_extras import auth, sessions
from google.appengine.ext import ndb
import logging
from User.handlers import AuthHandler	
from User.user import Instants,User
SERVER = 'gcm.googleapis.com'
PORT = 5235
USERNAME = "849208174002"
PASSWORD = "AIzaSyBNnXeISW8-KfETBKE-r0ASytx4WyC6NTk"

unacked_messages_quota = 1000
send_queue = []
def push_dbkey(push_dbname="push_db"):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('push_db', "push_db")

def group_dbkey(group_dbname="group_db"):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('group_db', "group_db")

class InstantMesg (ndb.Model):
    message = ndb.StringProperty(indexed=False)
    ohid = ndb.StringProperty()
    instanttype = ndb.StringProperty()
    atplace = ndb.StringProperty(indexed=False)
    userid = ndb.IntegerProperty(indexed=False)
    timestamp = ndb.DateTimeProperty(indexed=False)
    uniqueid = ndb.StringProperty()
    gcmtype = ndb.StringProperty()
class GcmData(ndb.Model):
    bid  = ndb.StringProperty()
    instants = ndb.StructuredProperty (InstantMesg, repeated=True)

class FriendsData(ndb.Model):
    state = ndb.StringProperty()
    userid = ndb.IntegerProperty()
    issmashed = ndb.StringProperty()

class GroupData(ndb.Model):
    uniqueid = ndb.StringProperty()
    bid = ndb.StringProperty() 
    bname = ndb.StringProperty()
    userid = ndb.IntegerProperty()
    friends = ndb.StructuredProperty(FriendsData,repeated=True)
    instants = ndb.StructuredProperty (InstantMesg, repeated=True)

def UpdateGCM(self,instanttype,ohurl):
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
	    instants = push.instants            
	    if len(instants) > 20:
		del instants[-1]
	    instant = InstantMesg(message = message,atplace = atplace,userid=self.user_id,timestamp = timestamp,instanttype = instanttype,ohid = ohurl)
	    instants.append(instant)
	    push.instants = instants
	    push.put()

	secs = calendar.timegm(timestamp.timetuple())

	#querry databse for registration ids
	user_query = User.query(User.instants.gcm_bids == bid)
	users = user_query.fetch() 	
	for user in users:
	    if user.key.id() != self.user_id:
		registration_ids.append(user.instants.gcm_regid)
	logging.info("%s" %registration_ids)
	if len(registration_ids) == 0:
	    self.response.write("")
	    return
	Bodyfields = {
	      "data": {"live":message,"username":userDetails.name,"bid":bid,"bname":bname,"atplace":atplace,"timestamp":secs,"instanttype":instanttype,'ohurl':ohurl},
	      "registration_ids": registration_ids
	     }
	result = urlfetch.fetch(url="https://android.googleapis.com/gcm/send",
			payload=json.dumps(Bodyfields),
			method=urlfetch.POST,
			headers={'Content-Type': 'application/json','Authorization': 'key=AIzaSyBNnXeISW8-KfETBKE-r0ASytx4WyC6NTk'})
	#self.response.out.write('Server response, status: ' + result.content )
        return result

class ExitGroup(AuthHandler):
    def get(self):
        uniqueid = self.request.get('uniqueid')
	group_query = GroupData.query(GroupData.uniqueid == uniqueid)	
	groups = group_query.fetch(1) 
        delsuccess = False
        uid = self.user_id
	for group in groups:
            for friend in group.friends:
                if friend.userid == uid:
                    friend.state = "out"
                    group.put()
                    delsuccess = True
        if delsuccess == True:
             self.response.write('success')
        else:
             self.response.write('failure')


class DeleteGroup(AuthHandler):
    def get(self):
        uniqueid = self.request.get('uniqueid')
        userid = self.user_id
	group_query = GroupData.query(GroupData.uniqueid == uniqueid)	
	groups = group_query.fetch(1) 
        delsuccess = False
        registration_ids = []
	for group in groups:
            if group.userid == userid:
                for friend in group.friends:
                    uid = friend.userid
                    if friend.state == 'in':
                        l_auth = auth.get_auth()
                        userData = l_auth.store.user_model.get_by_id (uid)
                        registration_ids.append(userData.instants.gcm_regid)
                group.key.delete()
                delsuccess = True
	if len(registration_ids) != 0:
	    Bodyfields = {
	      "data":{"instanttype":'delete','uniqueid':uniqueid},
	      "registration_ids": registration_ids
	     }
            result = urlfetch.fetch(url="https://android.googleapis.com/gcm/send",
			payload=json.dumps(Bodyfields),
			method=urlfetch.POST,
			headers={'Content-Type': 'application/json','Authorization': 'key=AIzaSyBNnXeISW8-KfETBKE-r0ASytx4WyC6NTk'})
        if delsuccess == True:
             self.response.write('success')
        else:
             self.response.write('failure')

class ResendRequests(AuthHandler):
    def get(self):
        uniqueid = self.request.get('uniqueid')
        userDetails = self.current_user
	group_query = GroupData.query(GroupData.uniqueid == uniqueid)	
	groups = group_query.fetch(1) 
        registration_ids = []
	for group in groups:
            bid = group.bid
            bname = group.bname
            for friend in group.friends:
                uid = friend.userid
                if friend.issmashed == 'true':
                    l_auth = auth.get_auth()
                    userData = l_auth.store.user_model.get_by_id (uid)
                    registration_ids.append(userData.instants.gcm_regid)

	#querry databse for registration ids
	logging.info("%s" %registration_ids)
	if len(registration_ids) == 0:
	    self.response.write("")
	    return
	Bodyfields = {
	      "data":{"username":userDetails.name,"bname":bname,"instanttype":'request','uniqueid':uniqueid},
	      "registration_ids": registration_ids
	     }
	result = urlfetch.fetch(url="https://android.googleapis.com/gcm/send",
			payload=json.dumps(Bodyfields),
			method=urlfetch.POST,
			headers={'Content-Type': 'application/json','Authorization': 'key=AIzaSyBNnXeISW8-KfETBKE-r0ASytx4WyC6NTk'})
	#self.response.out.write('Server response, status: ' + result.content )

        self.response.write('%s' %uniqueid)
        
class GroupGcmConfirm(AuthHandler):
    def get(self):
        state = self.request.get('state')
        regid = self.request.get('regid')
        uniqueid = self.request.get('uniqueid')
        userid = self.user_id
	group_query = GroupData.query(GroupData.uniqueid == uniqueid)	
	groups = group_query.fetch(1) 
        bid = ''
	for group in groups:
            bid = group.bid

        self.current_user.instants.gcm_regid = regid
        exists = False; 
        for sbid in self.current_user.instants.gcm_bids:
            if sbid == bid:
                exists = True
        if exists == False:
            self.current_user.instants.gcm_bids.append(bid)
        self.current_user.put() 
        group_query = GroupData.query(GroupData.uniqueid == uniqueid)	
	groups = group_query.fetch(1)
        finalDict = {}
        allFriends = [] 
	for group in groups:
            eachFriend = {}
            if group.userid != userid:
                l_auth = auth.get_auth()
                userData = l_auth.store.user_model.get_by_id (group.userid)
                if userData:
                    eachFriend['name'] = userData.name
                    eachFriend['avatar'] = userData.avatar_url
                    allFriends.append(eachFriend)
            for friend in group.friends:
                if friend.userid == userid:
                    friend.state = state
                else:
                    l_auth = auth.get_auth()
                    userData = l_auth.store.user_model.get_by_id (friend.userid)
                    if userData:
                        eachFriend['name'] = userData.name
                        eachFriend['avatar'] = userData.avatar_url
                        allFriends.append(eachFriend)
            group.put()
        finalDict['friends'] = allFriends
        finalDict['bid'] = bid
        self.response.write(json.dumps(finalDict))	        

def UpdateGcmGroup(self,instanttype,ohurl):
	uniqueid = self.request.get("uniqueid")
	bname = self.request.get("bname")
	message = self.request.get("message")
	atplace = self.request.get("atplace")
        bid = ''        
	timestamp = datetime.datetime.now()
	userid = self.user_id
	userDetails = self.current_user
	group_query = GroupData.query(GroupData.uniqueid == uniqueid)	
	groups = group_query.fetch(1) 
	registration_ids = []
        frienduserids = []
	for group in groups:
            bid = group.bid
            if group.userid != self.user_id:
                l_auth = auth.get_auth()
                userData = l_auth.store.user_model.get_by_id (group.userid)
                registration_ids.append(userData.instants.gcm_regid)                            
	    instants = group.instants            
	    if len(instants) > 20:
		del instants[-1]
	    instant = InstantMesg(message = message,atplace = atplace,userid=self.user_id,timestamp = timestamp,instanttype = instanttype,ohid = ohurl,gcmtype='group',uniqueid=uniqueid)
	    instants.append(instant)
	    group.instants = instants
            friends = group.friends
            for friend in friends:
                if friend.state == 'in':
                    frienduserids.append(friend.userid)
                    if self.user_id != friend.userid:
                        l_auth = auth.get_auth()
                        userData = l_auth.store.user_model.get_by_id (friend.userid)
                        registration_ids.append(userData.instants.gcm_regid)            
	    group.put()

	secs = calendar.timegm(timestamp.timetuple())
	logging.info("%s" %frienduserids)
	logging.info("%s" %registration_ids)
	if len(registration_ids) == 0:
	    self.response.write("")
	    return
	Bodyfields = {
	      "data": {"live":message,"username":userDetails.name,"bid":bid,"bname":bname,"atplace":atplace,"timestamp":secs,"instanttype":instanttype,'ohurl':ohurl,'uniqueid':uniqueid},
	      "registration_ids": registration_ids
	     }
	result = urlfetch.fetch(url="https://android.googleapis.com/gcm/send",
			payload=json.dumps(Bodyfields),
			method=urlfetch.POST,
			headers={'Content-Type': 'application/json','Authorization': 'key=AIzaSyBNnXeISW8-KfETBKE-r0ASytx4WyC6NTk'})
	#self.response.out.write('Server response, status: ' + result.content )
        return result

class GroupGcmStart(AuthHandler):
    def get(self):
        result = UpdateGcmGroup(self,"text",'')
        self.response.out.write('Server response, status: ' + result.content )
        
class GcMStart(AuthHandler):
    def get(self):
        result = UpdateGCM(self,"text",'')
        self.response.out.write('Server response, status: ' + result.content )

class MyGroupRegister(AuthHandler):
    def post(self):
        bid = self.request.get("bid")
        userStr = self.request.get("users")
        bname = self.request.get("bname")
        logging.info('thejjejje %s' %userStr)
        friends = json.loads(userStr)
        groupDb = GroupData(parent=group_dbkey("group_db"))
        groupDb.bid = bid
        groupDb.bname = bname
        uniqueid = str(uuid.uuid4()) 
        groupDb.uniqueid = uniqueid
        groupDb.userid = self.user_id
        userDetails = self.current_user
        frienduserids = []        
        registration_ids = []
        for friend in friends['friends']:
            uid = friend['userid']
            frienduserids.append(uid)
            issmashed = friend['issmashed']
            friendData = FriendsData(state = 'out',userid = uid,issmashed = issmashed)
            groupDb.friends.append(friendData)
            if issmashed == 'true':
                l_auth = auth.get_auth()
                userData = l_auth.store.user_model.get_by_id (uid)
                registration_ids.append(userData.instants.gcm_regid)
        groupDb.put()
	#querry databse for registration ids
	logging.info("%s" %registration_ids)
	if len(registration_ids) == 0:
	    self.response.write('%s' %uniqueid)
	    return
	Bodyfields = {
	      "data":{"username":userDetails.name,"bname":bname,"instanttype":'request','uniqueid':uniqueid},
	      "registration_ids": registration_ids
	     }
	result = urlfetch.fetch(url="https://android.googleapis.com/gcm/send",
			payload=json.dumps(Bodyfields),
			method=urlfetch.POST,
			headers={'Content-Type': 'application/json','Authorization': 'key=AIzaSyBNnXeISW8-KfETBKE-r0ASytx4WyC6NTk'})
	#self.response.out.write('Server response, status: ' + result.content )

        self.response.write('%s' %uniqueid)
        
        
class GcmRegister(AuthHandler):
    def get(self):
        regid = self.request.get("regid");
        bid = self.request.get("bid") 
        userid = self.user_id
        if self.current_user.instants == None:
            self.current_user.instants = Instants(gcm_bids = [""],gcm_regid = "")
            self.current_user.put() 
        self.current_user.instants.gcm_regid = regid
        exists = False; 
        for sbid in self.current_user.instants.gcm_bids:
            if sbid == bid:
                exists = True
        if exists == False:
            self.current_user.instants.gcm_bids.append(bid)
        self.current_user.put() 

        push_query = GcmData.query(GcmData.bid == bid)	
        pushes = push_query.fetch(1) 

        finalDict = {}
        allmessages = []
        bidExists = False;
        for push in pushes:
            i = 0
            bidExists = True
            for instant in push.instants:
                messageDict = {}
                messageDict['message'] = instant.message
                l_auth = auth.get_auth()
                userData = l_auth.store.user_model.get_by_id(push.instants[i].userid)
                messageDict['username'] = userData.name
                messageDict['atplace'] = push.instants[i].atplace
                messageDict['instanttype'] = push.instants[i].instanttype
                messageDict['ohurl'] = push.instants[i].ohid
                secs = calendar.timegm(push.instants[i].timestamp.timetuple())
                messageDict['timestamp'] = secs
                if push.instants[i].userid == self.user_id:
                    messageDict['self'] = 'true'
                else:
                    messageDict['self'] = 'false'
                i = i + 1
                allmessages.append(messageDict)
        finalDict['messages'] = allmessages
        if bidExists == False:
            pushdb = GcmData(parent=push_dbkey("push_db"))
            pushdb.bid = bid
            pushdb.put()    
        self.response.write(json.dumps(finalDict))	        


import webapp2
import logging
import uuid
import cgi
import urllib
from webapp2_extras import auth, sessions
import os
from google.appengine.api import users

from google.appengine.ext import ndb
from User.handlers import AuthHandler


class CommentDb(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    userid = ndb.IntegerProperty()
    commentid = ndb.StringProperty()
    parentid = ndb.StringProperty()
    comment = ndb.StringProperty()
    commentohurl = ndb.StringProperty()
    
    
def CreateComment (reviewDict,parentid,userid):
    comment = CommentDb(parent=ndb.Key('comment_oh','comment_oh'))
    comment.userid = userid
    comment.commentid = str(uuid.uuid4())
    if parentid == 'init':
        comment.parentid = comment.commentid
    else:
        comment.parentid = parentid
    if reviewDict:
        comment.comment = reviewDict.get('comment')
        comment.commentohurl = reviewDict.get('commentohurl')
    comment.put()

    return str(comment.commentid)
        
        
class AddCommentOh (AuthHandler):
    def get(self):
        user_dict = self.auth.get_user_by_session()
        userId = user_dict['user_id']        
        commentid = CreateComment(self.request, self.request.get('commentid'),userId)
        self.response.write('%s' %commentid)     
        

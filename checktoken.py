import os
import webapp2
from google.appengine.ext import ndb
from secrets import secrets
from User.handlers import AuthHandler
from MemeCreator.storeimage import UserMemeDb
USER_MEME_DB_NAME = 'user_meme_db'

def user_meme_dbkey(meme_userdbname=USER_MEME_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('user_meme_db', meme_userdbname)
class BaseRequestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write ("theju%s" % self.request)  
        
class MigrationOH(AuthHandler):
    def get(self):
        sadmin = secrets.CheckSuperAdminRights(self.user_id) 
        if sadmin == True:
            u_q = UserMemeDb.query(ancestor=user_meme_dbkey(USER_MEME_DB_NAME)).order(-UserMemeDb.date)
            memes = u_q.fetch()
            for meme in memes:
                meme.mode = 'gallery'
                meme.put()
            self.response.write('done')
        else:
            self.response.write('Not allowed')
        
#https://www.facebook.com/dialog/oauth?client_id=xxxxxxx&redirect_uri=http://smashed.in/gettoken&scope=manage_pages

#https://graph.facebook.com/oauth/access_token?client_id=xxxxxx&redirect_uri=http://smashed.in/gettoken&client_secret=xxxxxx&code=AQAPqKtA27TCQCtw8qt7aPxLK9RgiHeMif6pZr5Ww8zYVTr2trcK0jD38FN0G5QFZQ5vo4BVqrtCGPVAqFujUrXt5mCqNUHhXtvk9xN5f5ZJy6c2ffiJeWvt8a9bUz3zzd6zfgjn_XvqaZK7L1nLhXQVHfi9aoL5VH4AkNH5tolquCV5Vlf7sVsRJnQVtl3cqtrK0SXvofUZFuagB8bHzc5tiBlP0EaRkWyOzTF3r44CKpKEB7PG6cYWi71oqYm7jxWO1byFIe3QLYJN74NBJNgNXBoqSuuCuuS8QwjjNSTqjfoBcF39p-4DQ3_EakxZcQA

#https://graph.facebook.com/smashed.in.7/accounts
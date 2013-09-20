import webapp2

import cgi
import urllib

from google.appengine.api import users

from google.appengine.ext import ndb

from google.appengine.api import images

from google.appengine.ext import db

MEME_DB_NAME = 'meme_db'


def meme_dbkey(meme_dbname=MEME_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('meme_db', meme_dbname)



class MemeDb(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    content = ndb.BlobProperty()
    icon    = ndb.BlobProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    myid   = ndb.StringProperty()


class ListFiles(webapp2.RequestHandler):

    def get(self):
        meme_dbname = self.request.get('meme_db',MEME_DB_NAME)
        meme_query = MemeDb.query(ancestor=meme_dbkey(meme_dbname)).order(-MemeDb.date)
        memes = meme_query.fetch(10)

        self.response.write('<head>')
        for meme in memes:
            self.response.write('<url>')
            self.response.write('/actions/icon?id=%s' %
                                meme.myid)
            self.response.write('</url>')
        self.response.write('</head>')

		
MAIN_PAGE_FOOTER_TEMPLATE = """\
<head>
<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
    <script src="http://cdn.jquerytools.org/1.2.7/full/jquery.tools.min.js"></script>
  <!--script src="http://code.jquery.com/jquery-1.9.1.js"></script!-->
  <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
  <script  src="./assets/meme.js"></script>
  </head>
    <form action="/actions/store?%s" method="post" enctype="multipart/form-data">
      <input name="content" type="file" />
	  <input type="text" name='id' value="%s"/>
      <div><input type="submit" value="Store Meme"></div>
    </form>
	<input type="file" id="myFile" style="display:none;">
</html>
"""

class MainPageStore(webapp2.RequestHandler):

    def get(self):
        self.response.write('<html><body>')
        lastid = int(self.request.get('id'))
        lastid = lastid + 1
        meme_query = MemeDb.query(ancestor=meme_dbkey(MEME_DB_NAME)).order(-MemeDb.date)
        memes = meme_query.fetch(10)

        for meme in memes:
            query_params = {'id': meme.myid}				
            self.response.write('<img src="/actions/icon?' + urllib.urlencode(query_params) + '"/>')

			# Write the submission form and the footer of the page
        sign_query_params = urllib.urlencode({'meme_db': MEME_DB_NAME})
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE %
                            (sign_query_params,lastid))




class Store(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        meme_dbname = self.request.get('meme_db',
                                          MEME_DB_NAME)
        meme = MemeDb(parent=meme_dbkey(meme_dbname))

        meme.myid = self.request.get('id')
        meme.content = self.request.get('content')
        icon = images.resize(meme.content, 200, 200)
        meme.icon = db.Blob(icon)
        meme.put()

        query_params = {'id': meme.myid}
        self.redirect('/actions/storeview?' + urllib.urlencode(query_params))

class GetFile(webapp2.RequestHandler):

    def get(self):
        myId=self.request.get('id')
        
        meme_dbname = self.request.get('meme_db',MEME_DB_NAME)
        meme_query = MemeDb.query(ancestor=meme_dbkey(meme_dbname)).order(-MemeDb.date)
        memes = meme_query.fetch(10)


        for meme in memes:
            if meme.myid == myId:
                self.response.write('%s' %
                                meme.icon)

class GetIcon(webapp2.RequestHandler):

    def get(self):
        myId=self.request.get('id')
        
        meme_dbname = self.request.get('meme_db',MEME_DB_NAME)
        meme_query = MemeDb.query(ancestor=meme_dbkey(meme_dbname)).order(-MemeDb.date)
        memes = meme_query.fetch(10)


        for meme in memes:
            if meme.myid == myId:
                self.response.write('%s' %
                                meme.content)
								
application = webapp2.WSGIApplication([
    ('/actions/storeview', MainPageStore),
	('/actions/list',ListFiles),
	('/actions/store', Store),
	('/actions/icon',GetFile),
    	('/actions/file',GetIcon),
], debug=True)

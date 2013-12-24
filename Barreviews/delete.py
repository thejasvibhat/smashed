import webapp2
import logging
from google.appengine.api import search
from User.handlers import AuthHandler
from storereview import ReviewDb
REVIEW_DB_NAME = 'bars_db'
_INDEX_NAME = 'localityTagSearch'

def review_dbkey(review_dbname=REVIEW_DB_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('bars_db', review_dbname)

class BDeleteHandler (AuthHandler):
    def get(self):
        self.user_gatekeeper ()
        self._gatekeeper ()
        bid = self.request.get('bid')
        review_query = ReviewDb.query(ReviewDb.bid == bid)        
        reviews = review_query.fetch()
        for review in reviews:
            review.key.delete()
        expr_list = [search.SortExpression(
            expression='bid', default_value='',
            direction=search.SortExpression.DESCENDING)]
        # construct the sort options
        sort_opts = search.SortOptions(
             expressions=expr_list)
        query_options = search.QueryOptions(
            limit=100,
            sort_options=sort_opts)
        q = 'bid:%s'%bid
        query_obj = search.Query(query_string=q, options=query_options)
        results = search.Index(name=_INDEX_NAME).search(query=query_obj)
        indexes = search.Index(name=_INDEX_NAME)
        for result in results:
            logging.info('%s'%result)
            indexes.delete(result.doc_id)

        self.response.out.write('deleted')

    def _gatekeeper (self):
        if self.user.hasPermission.editBar is True:
            return
        self.abort (403)

            


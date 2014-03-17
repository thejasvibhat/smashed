
#some stackoverflow link.

from google.appengine.ext import ndb
from webapp2_extras.appengine.auth.models import User as Webapp2User

#Move this to acl.py if it grows
class Permission (ndb.Model):
    addBar = ndb.BooleanProperty(default=False, required=True)
    editBar = ndb.BooleanProperty(default=False, required=True)

    #UC: Hooks don't seem to work in StructuredProperty
    # def _pre_put_hook (self):
    #     if self.addBar == True:
    #         self.editBar = True

    # @classmethod
    # def _post_get_hook(cls, key, future):
    #     obj = future.get_result()
    #     if obj is not None:
    #         if obj.addBar == True:
    #             obj.editBar = True

class Instants (ndb.Model):
    gcm_bids = ndb.StringProperty (repeated=True)
    gcm_reg = ndb.StringProperty ()
    gcm_lastseen = ndb.DateTimeProperty ()

class User(Webapp2User):
    usertype = ndb.StringProperty (repeated=True)
    hasPermission = ndb.StructuredProperty (Permission)
    instants = ndb.StructuredProperty (Instants)

    @classmethod
    def _post_get_hook(cls, key, future):
        obj = future.get_result()
        if obj.hasPermission is None:
            obj.hasPermission = Permission()
        else:
            if obj.hasPermission.addBar == True:
                obj.hasPermission.editBar = True

    def _pre_put_hook (self):
        if self.hasPermission is None:
            self.hasPermission = Permission()
        else:
            if self.hasPermission.addBar == True:
                self.hasPermission.editBar = True

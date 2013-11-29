import os
import webapp2
class BaseRequestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write ("theju%s" % self.request)  
		
#https://www.facebook.com/dialog/oauth?client_id=252676761554370&redirect_uri=http://smashed.thjeasvi.in/gettoken&scope=publish_stream

#https://graph.facebook.com/oauth/access_token?client_id=252676761554370&redirect_uri=http://smashed.thejasvi.in/gettoken&client_secret=f47dc57744f2abe248beb705fde437f6&code=AQAQwCWzJfYHsxO-mSKU8QKOM5GZZSqjVAYRV0cGecrzkWvZvx_iR6u7XYyO_32aI1q6v6Pvadz8u05Eh0zTWezJskwa62joqdV31B2WRiSXY_uGq_ZEQONq9tSlVISjMZrGFAr2Hkjdr_jzkf54c-8mHCycdgR1e2DIMueqwBrKSrCwWq05ZqVq0BMyoEe49px6_QppKZigu2BdgS8kbUU9kW8XSi-E7IR5isSv9HNmgXbKoSElRKnwYLavhZ4K8OkS1eLNnCDyCKgOs-KJBiI7fbHFAClibKwg2nsOm_lDgISlG-e78n97LkO31BTNWf4
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from outbound import OutboundHandler
from inbound import InboundHandler

_DEBUG = False

class TestEmail():
	"""
	1. Create an object that has everything I need
	2. Convert the object into JSON.
	3. Done.
	4. Eventually make this into a function that takes the appropriate values.
	"""
	def __init__(self, key, to, cc, bcc, reply_to, subject, body=None,
	 			 html=None):
		self.headers = {}
		self.headers["Authorization"] = key #check Authorization, Check key
		self.headers["to"] = to
		self.headers["cc"] = cc
		self.headers["bcc"] = bcc
		self.headers["reply_to"] = reply_to
		self.headers["subject"] = subject
		if body:
			self.headers["body"] = body
		elif html:
			self.headers["html"] = html
		else:
			raise error.# Fix this
	

class SendTestEmailHandler(webapp.RequestHandler):
	"""
	1. Call function to create an email object with all the details we need and be returned JSON
	2. Take the JSON and pass it to the correct URL.
	3. Done.
	"""


# Map URLs to our RequestHandler classes
_URLS = [
   ('/emails(\.json)*', OutboundHandler), 
   ('/SendTestEmail', SendTestEmailHandler),
   InboundHandler.mapping()
]

def main():
  application = webapp.WSGIApplication(_URLS, debug=_DEBUG)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()

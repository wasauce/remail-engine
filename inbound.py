import logging, email, yaml
from models import store_email_and_attachment
from django.utils import simplejson as json
from google.appengine.ext import webapp, deferred
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api.urlfetch import fetch
from google.appengine.api.urlfetch import Error as FetchError

settings = yaml.load(open('settings.yaml'))

def callback(message):
  
  result = {'email': 
                  { 'raw': message.original.as_string(True),
                    'sender':message.sender, 
                    'subject':message.subject, 
                    'to': message.to,
                    'date':message.date
                    }
            }
  store_email_and_attachment()
  
  response = fetch(settings['outbound_url'], 
              payload=json.dumps(result), 
              method="POST", 
              headers={
                'Authorization': settings['api_key'],
                'Content-Type': 'application/json'
              },
              deadline=10
             )

  logging.info(response.status_code)
  if response.status_code != 200:
    raise FetchError()

class InboundHandler(InboundMailHandler):
    def receive(self, message):
      logging.info("Received a message from: " + message.sender)
      deferred.defer(callback, message, _queue='inbound')
import logging, yaml
from models import store_email_and_attachment

from django.utils import simplejson as json
from google.appengine.ext import webapp, deferred
from google.appengine.api import mail

settings = yaml.load(open('settings.yaml'))

def safe_dict(d): 
  """
    Recursively clone json structure with UTF-8 dictionary keys
    http://bugs.python.org/issue2646
  """ 
  if isinstance(d, dict): 
    return dict([(k.encode('utf-8'), safe_dict(v)) for k,v in d.iteritems()]) 
  elif isinstance(d, list): 
    return [safe_dict(x) for x in d] 
  else: 
    return d

def email(body):
  email = json.loads(body)
  logging.info(email)
  mail_message = mail.EmailMessage(**safe_dict(email))
  mail_message.send()

  #The below stores the email and any attachments
  stored_email = store_email_and_attachment(mail_message,
											is_from_external=False)
  if not stored_email:
    logging.error("Failed to save message: %s", 
                  message.original.as_string(True))


class OutboundHandler(webapp.RequestHandler):

  def post(self, *args):
    api_key = self.request.headers.get('Authorization')
    
    if api_key != settings['api_key']:
      logging.error("Invalid API key: " + str(api_key))
      self.error(401)
      return
    
    deferred.defer(email, self.request.body, _queue='outbound')

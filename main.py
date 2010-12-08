from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from outbound import OutboundHandler
from inbound import InboundHandler

_DEBUG = False

class SendTestEmailHandler(webapp.RequestHandler):
  """
    
  """


### code from ruby
  Email.headers["Authorization"] = key

class Email < ActiveResource::Base
  self.timeout = 5
  self.format  = :json
  self.include_root_in_json = false
  
  cattr_accessor :headers
  @@headers = {}
  
  schema do
    string :sender, :to, :cc, :bcc,
           :reply_to, :subject,
           :body, :html
  end
  
  validates_presence_of :sender, :to, :subject
  validates_presence_of :body, :unless => :html?

  # The sender address must be the email address of a 
  # registered administrator for the application    
  def from=(address)
    self.sender = address
  end
end

class ActionMailer
  def initialize(settings)
    settings.each {|key, value| 
      Remail.send("#{key}=", value) 
    }
  end
      
  def deliver!(mail)
    remail = Remail::Email.new
    
    %w{to from cc bcc reply_to}.each {|attr|
      value = mail.send(attr)
      next unless value
      remail.send("#{attr}=", value.join(", "))
    }      
    
    remail.subject  = mail.subject
    
    text_body   = mail.text_part ? mail.text_part.body : mail.body
    html_body   = mail.html_part && mail.html_part.body
    remail.body = text_body.encoded if text_body
    remail.html = html_body.encoded if html_body
    
    remail.save!

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

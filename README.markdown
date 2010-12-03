Remail is RESTful email for any web app.

Forget configuring SMTP servers and queues, just use Remail. 
Remail uses Google App Engine to send and receive emails RESTfully.

## Features
* ActionMailer handler POSTs emails to your Remail App Engine in order to send them
* Remail handler POSTs received emails back to a configurable URL
  * Remail will sent an Email hash with the following attributes:
    * raw - The raw content of the message
    * sender - Whom sent it
    * subject - The subject of the incoming message
    * to - Who it was intend it to
    * date - Send date of the message
    
* Remail will retry the callback if the endpoint is not available

## Setup
* Configure settings.yaml:
  * Create a random api_key, for example using uuidgen.
  * Add a publicly accessible callback url as the outbound_url.
* [Create](https://appengine.google.com/) a Google App Engine application.
* Configure app.yaml with the new app id.
* Upload the engine to Google App Engine (see their [docs](http://code.google.com/appengine/docs))
* DONE. Now go send/receive some email.
  * Ruby users consider installing the [Remail gem](http://github.com/maccman/remail) (sudo gem install remail).
  * Python users consider reviewing a python example []() (git clone the project)

For the python project I need:
Read: http://code.google.com/appengine/docs/python/mail/overview.html

0) Research into sending an email address and put this into the Read me documentation. Information on how to associate this with other email addresses.
1) A handler that allows me to send email based on subject and a body and an attachment that I send to a TO email address
1.1) A concept of turning on admin functionality 
2) A handler that receives updates and stores the data in a DB.
3) A handler that shows what updates are in the DB.


## Feature ideas
* Attachment support. Add support to send attachments and receive and store and resend attachments -- http://code.google.com/appengine/docs/python/mail/attachments.html


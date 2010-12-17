Remail is RESTful email for any web app.

Forget configuring SMTP servers and queues, just use Remail. 
Remail uses Google App Engine to send and receive emails RESTfully.

## Features
* POST emails to your Remail App Engine in order to send them
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
  * Ruby users consider installing the [Remail gem](http://github.com/maccman/remail) (sudo gem install remail) to more easily send/receive emails.
  * Python users consider reviewing a python example found in main.py as the SendTestEmailHandler
* Note that there are multiple options for the email address FROM which the email is sent. Specifically it can be an email address of a registered administrator (developer) of the application, the current user if signed in with Google Accounts, or any valid email receiving address for the app (that is, an address of the form string@appid.appspotmail.com). See [more details here.](http://code.google.com/appengine/docs/python/mail/overview.html)
  * For a more professional/official looking emails, register an email address from your domain as an administrator (developer) of the application and send all emails from that address -- e.g. support@mydomain.com.


## Feature ideas
* 

## Todo
* Add example python code to call the App
* Ensure that attachments are properly being stored 
* Send the administrators of the app an email alerting them that email has been received.
* Determine how to restructure my class so that I don't have to define each header.

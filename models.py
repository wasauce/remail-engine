"""
Database models for storing emails and any associated attachments.

Additionally included are helper functions for creating models.
"""

import logging, yaml
import email
from google.appengine.ext import db
from google.appengine.api import mail

settings = yaml.load(open('settings.yaml'))

  
class Email(db.Model):
	has_attachment = BooleanProperty()
	is_from_external = BooleanProperty()
	raw = StringProperty(multiline=True)
	sender = StringProperty()
	subject = StringProperty()
	to = StringProperty()
	auto_now_add = DateTimeProperty(auto_now_add=True)
	date = DateTimeProperty()


class Attachment(db.Model):
	file_name = StringProperty()
	file_blob = BlobProperty()
	email = ReferenceProperty(reference_class=Email)


def send_email_to_admin(subject, body):
	""" Sends email to the admins of the site.
	"""
	# mail_admin must be an admin of the app. app_admin set in settings.yaml
    mail_admin = settings['app_admin']

	subject = 'REMAIL APP: ' + subject
	mail.send_mail_to_admins(sender=mail_admin,
                             subject=subject,
                             body=body)



def create_new_attachment(file_name, file_blob, email):
	"""Function to store an attachment in the database."""
	
	new_attachment = Attachment()
	new_attachment.file_name = file_name
	new_attachment.file_blob = file_blob
	new_attachment.email = email

	try:
		new_attachment.put()
		logging.info('Saved an new attachment.')
		return new_attachment
	except:
		subject = 'Failed to create attachment.'
		body = 'Email with which there was a failed message: %s' % str(email)
		send_email_to_admin(subject, body)
		return None


def create_new_email(raw, sender, subject, to, date, has_attachment,
					 is_from_external=True):
	"""Function to store an email in the database."""

    if has_attachment:
	  attachment = True
	else:
	  attachment = False

	new_email = Email()
	new_email.has_attachment = attachment
	new_email.is_from_external = is_from_external
	new_email.raw = raw
	new_email.sender = sender
	new_email.subject = subject
	new_email.to = to
	if date:
		new_email.date = date

	try:
		new_email.put()
		logging.info('Saved a new email.')
		return new_email
	except:
		subject = 'Failed to save a new email.'
		body = 'Email with which there was a failed message: %s' % str(raw)
		send_email_to_admin(subject, body)
		return None
		

def store_email_and_attachment(message, is_from_external=True):
	"""Function to store a message in the database."""
    
	date = email.utils.parsedate(message.date)

	email = create_new_email(message.original.as_string(True), message.sender, 
							 message.subject, message.to, date,
							 message.attachments, is_from_external)

	if message.attachments:
		for filename, contents in message.attachments:
			attachment = create_new_attachment(filename, contents, email)

	return email

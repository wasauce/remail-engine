
"""
File contains database models for storing emails and any associated attachments.

TODO:
--Finish the date parsers and the functions for saving
--Test to see if they work as intended
--import into inbound.py to process inbound emails
--import into outbound to save outbound emails
--make the test instance that can be hit with requests
--fire test emails at it
--write a library / util to send these emails in tornado

"""

import logging
import email
from google.appengine.ext import db

  
class Email(db.Model):
	has_attachment = BooleanProperty()
	is_incoming = BooleanProperty()
	raw = StringProperty(multiline=True)
	sender = StringProperty()
	subject = StringProperty()
	to = StringProperty()
	auto_now_add = DateTimeProperty(auto_now_add=True)
	date = DateTimeProperty()

class Attachment(db.Model):
	is_incoming = BooleanProperty()
	file_name = StringProperty()
	file_blob = BlobProperty()
	email = ReferenceProperty(reference_class=Email)


def create_new_attachment(file_name, file_blob, email, is_incoming=True):
	"""Function to store an attachment in the database."""
	
	new_attachment = Attachment()
	new_attachment.is_incoming = is_incoming
	new_attachment.file_name = file_name
	new_attachment.file_blob = file_blob
	new_attachment.email = email

	try:
		new_attachment.put()
		logging.info('Saved an new attachment.')
		return new_attachment

def create_new_email(raw, sender, subject, to, date, attachment, 
					 has_attachment=False, is_incoming=True):
	"""Function to store an email in the database."""

	new_email = Email()
	new_email.has_attachment = is_incoming
	new_email.is_incoming = file_name
	new_email.raw = raw
	new_email.sender = sender
	new_email.subject = subject
	new_email.to = to
	new_email.date = date

	try:
		new_email.put()
		logging.info('Saved an new email.')
		return new_email

def store_email_and_attachment(message, outbound=True):
	"""Function to store a message in the database."""
    


	date = email.utils.parsedate(message.date)
	email = create_new_email(message.original.as_string(True), message.sender, 
							 message.subject, message.to, )


	for filename, contents in message.attachments:
		attachment = create_new_attachment(filename, contents)

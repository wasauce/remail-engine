
"""
File contains database models for storing emails and any associated attachments.

TODO:
--Test to see if they work as intended
--make the test instance that can be hit with requests
--fire test emails at it
--write a library / util to send these emails in tornado

"""

import logging
import email
from google.appengine.ext import db

  
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

def create_new_email(raw, sender, subject, to, date, has_attachment,
					 is_from_external=True):
	"""Function to store an email in the database."""

	new_email = Email()
	new_email.has_attachment = has_attachment
	new_email.is_from_external = is_from_external
	new_email.raw = raw
	new_email.sender = sender
	new_email.subject = subject
	new_email.to = to
	if date:
		new_email.date = date

	try:
		new_email.put()
		logging.info('Saved an new email.')
		return new_email

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

from flask import current_app
import os
import secrets

from app.models.database import db
from app.utils import hash, Emailer
from app.utils.exceptions import EmailNotRegistered


# Send an email with a link for password reset
def requestPassReset(email: str) -> None:
	"""
	Request password reset to email by sending email w/ link
	"""

	# Determine if email is registered
	registered = db().fetch(f"""
		SELECT id, name FROM users
		WHERE email_hash='{hash(email)}';
	""")

	if len(registered) == 0:
		raise EmailNotRegistered()
	
	uuid = registered[0][0]
	name = registered[0][1]

	# Clear any pre-existing password reset requests
	db().modify(f"""
		DELETE FROM pass_reset
		WHERE user='{uuid}';
	""") 
	
	# === CREATE PASSWORD RESET REQUEST ===

	# Create password reset token
	token = secrets.token_urlsafe(64)

	# Register to db
	db().modify(f"""
		INSERT INTO pass_reset (user, code)
		VALUES ('{uuid}', '{hash(token)}');
	""")

	# === SEND EMAIL ===

	# Get email template
	with open(os.path.join(current_app.config['ASSETS_FOLDER'], 'passReset.html'), 'r') as file:
		content = file.read()

	# Insert link
	link = current_app.config['FRONTEND_URL'] + f'/passwordRequest?token={token}'

	content.replace('{{RESET_LINK}}', link)
	content.replace('{{RECIPIENT_NAME}}', name)

	# Send email
	Emailer().sendEmail(name, email, 'Password Reset Request Link', content)

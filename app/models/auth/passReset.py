from flask import current_app
import os
import secrets

from app.models.database import db
from app.utils import hash, Emailer, checkPasswordFormat
from app.utils.exceptions import EmailNotRegistered, InvalidPassword, InvalidPasswordResetRequest


# Send an email with a link for password reset
def requestPassReset(email: str) -> None:
	"""
	Request password reset to email by sending email w/ link
	"""

	delOldRequests()

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


# Actually change password
def resetPassword(token: str, password: str) -> None:
	"""
	Change the user's password to given password
	"""

	delOldRequests()

	# Validate password
	if checkPasswordFormat(password) == False:
		raise InvalidPassword()
	
	# Attempt to retrieve connected UUID
	user = db().fetch(f"""
		SELECT user FROM pass_reset
		WHERE code='{hash(token)}';
	""")

	if len(user) == 0:
		raise InvalidPasswordResetRequest()
	
	# Change user's password
	db().modify(f"""
		UPDATE users
		SET pass='{hash(password)}'
		WHERE id='{user[0][0]}';
	""")

	# Clear password reset requests
	db().modify(f"""
		DELETE FROM pass_reset
		WHERE user='{user[0][0]}';
	""") 


# Delete old password reset requests
def delOldRequests() -> None:
	"""
	Delete old password reset request tokens
	"""

	db().modify("""
		DELETE FROM pass_reset
		WHERE created < NOW() - INTERVAL '1 hour';
	""")

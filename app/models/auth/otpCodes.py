import os
import secrets
from flask import current_app

from app.models.database import db
from app.utils import hash, Emailer


# Send OTP Code
def sendCode(name: str, uuid: str, email: str) -> None:
	"""
	Send One-Time Password to given email
	"""

	# Generate 6-digit OTP code
	code = str(secrets.randbelow(900000) + 100000)

	# Get OTP email template
	with open(os.path.join(current_app.config['ASSETS_FOLDER']), 'otp.html', 'r') as file:
		content = file.read()

	# Insert code + name
	content.replace('{{OTP_CODE}}', code)
	content.replace('{{RECIPIENT_NAME}}', name)

	# Send email
	Emailer().sendEmail(name, email, 'Your One-Time Passcode for Chronosuite', content)


# Check OTP Code
def checkCode(uuid: str, code: str) -> None:
	"""
	Check OTP code against database
	"""

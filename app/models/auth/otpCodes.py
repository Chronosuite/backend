import os
import secrets
from flask import current_app

from app.models.database import db
from app.utils import hash, Emailer
from app.utils.exceptions import OTPAlreadySent, OTPWrongDevice


# Send OTP Code
def sendCode(name: str, uuid: str, email: str, ip: str, agent: str) -> None:
	"""
	Send One-Time Password to given email
	"""

	delOldCodes()

	# Generate 6-digit OTP code
	code = str(secrets.randbelow(900000) + 100000)

	# === REGISTER CODE ===
	
	# Determine if code for UUID already exists to not spam and wasn't recently sent
	sentCodes = db().fetch(f"""
		SELECT id FROM otp_codes
		WHERE user='{uuid}' AND created < NOW() - INTERVAL '1 minute';
	""")

	if len(sentCodes) != 0:
		raise OTPAlreadySent()
	else:
		# Delete pre-existing codes for this user
		db().modify(f"""
			DELETE FROM otp_codes
			WHERE user='{uuid}';
		""")

		# Register new code
		db().modify(f"""
			INSERT INTO otp_codes (ip, agent, code_num, user)
			VALUES ('{hash(ip)}', '{hash(agent)}', '{hash(code)}', '{uuid}');
		""")

	# === SEND EMAIL ===

	# Get OTP email template
	with open(os.path.join(current_app.config['ASSETS_FOLDER'], 'otp.html'), 'r') as file:
		content = file.read()

	# Insert code + name
	content.replace('{{OTP_CODE}}', code)
	content.replace('{{RECIPIENT_NAME}}', name)

	# Send email
	Emailer().sendEmail(name, email, 'Your One-Time Passcode for Chronosuite', content)


# Check OTP Code
def checkCode(userIP: str, userAgent: str, uuid: str, code: str) -> bool:
	"""
	Check OTP code against database
	"""

	delOldCodes()

	# Search database for match
	check = db().fetch(f"""
		SELECT id, ip, agent FROM otp_codes
		WHERE user='{uuid}' AND code_num='{hash(code)}';
	""")

	# Determine if OTP code was checked from the right device
	ip = check[1]
	agent = check[2]

	if hash(userIP) != ip or hash(userAgent) != agent:
		raise OTPWrongDevice()

	return not (len(check) == 0)


# Delete old codes
def delOldCodes() -> None:
	"""
	Delete expired codes
	"""

	db().modify("""
		DELETE FROM otp_codes
		WHERE created < NOW() - INTERVAL '10 minutes';
	""")

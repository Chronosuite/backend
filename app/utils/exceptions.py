# Custom Exceptions


class FailedEmail(Exception):
	"""Failed to send email to given email address"""


class InvalidPassword(Exception):
	"""Password does not meet password requirements"""


class InvalidEmail(Exception):
	"""Email is of an invalid format"""


class WrongOTP(Exception):
	"""OTP Code is wrong"""


class OTPAlreadySent(Exception):
	"""OTP code was already sent within 1 minute"""


class OTPWrongSession(Exception):
	"""OTP code was used for the wrong session"""

class NeedOTP(Exception):
	"""OTP code is needed for login"""


class ExpiredSession(Exception):
	"""Session does not exist or has been expired"""


class NoAccess(Exception):
	"""When attempting to modify something the user has no access to"""


class EmailAlreadyRegistered(Exception):
	"""The email is already registered to another user"""


class EmailNotRegistered(Exception):
	"""The email is not registered to any user"""


class WrongCredentials(Exception):
	"""Given credentials does not match any recorded user credentials"""


class InvalidPasswordResetRequest(Exception):
	"""Password reset request is invalid"""


class RequestBodyException(Exception):
	"""Error with the request body"""

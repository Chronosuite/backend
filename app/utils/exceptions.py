# Custom Exceptions


class FailedEmail(Exception):
	"""Failed to send email to given email address"""


class WrongOTP(Exception):
	"""OTP Code is wrong"""


class OTPAlreadySent(Exception):
	"""OTP code was already sent within 1 minute"""


class WrongCredentials(Exception):
	"""Given credentials does not match any recorded user credentials"""


class RequestBodyException(Exception):
	"""Error with the request body"""

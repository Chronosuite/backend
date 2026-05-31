# Custom Exceptions


class FailedEmail(Exception):
	"""Failed to send email to given email address"""


class WrongOTP(Exception):
	"""OTP Code is wrong"""


class WrongCredentials(Exception):
	"""Given credentials does not match any recorded user credentials"""

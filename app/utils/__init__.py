# Basic Functions

from hashlib import sha256

from app.utils.emailer import Emailer


def hash(txt: str) -> str:
	"""
	Use the SHA256 hashing algorithm to hash the given text
	"""

	return sha256(txt.encode('utf-8')).hexdigest()

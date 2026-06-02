# Basic Functions

from hashlib import sha256
from flask import current_app

from app.utils.emailer import Emailer
from app.utils.exceptions import RequestBodyException


def hash(txt: str) -> str:
	"""
	Use the SHA256 hashing algorithm to hash the given text
	"""

	return sha256(txt.encode('utf-8')).hexdigest()


def checkStructure(structure: dict[str], content: dict[str], path: str = "") -> dict[str]:
	"""
	Recursive helper function to check the structure of requests
	"""

	if isinstance(content, dict):
		for key, value in structure.items():
			full_key = f"{path}.{key}" if path else key
			if key not in content:
				raise RequestBodyException(f'Missing {full_key} parameter in body.')
			
			if type(value) != type(content[key]):
				raise RequestBodyException(f'Wrong data type for {full_key}. Expected {type(value).__name__}')
			
			if isinstance(value, (dict, list)):
				checkStructure(value, content[key], full_key)

	elif isinstance(content, list):
		if len(structure) == 0:
			return  # Allow empty list template, no further type checking
		
		check = structure[0]
		check_type = type(check)
		
		for i, item in enumerate(content):
			item_path = f"{path}[{i}]"
			if type(item) != check_type:
				raise RequestBodyException(f'Wrong data type for {item_path}. Expected {check_type.__name__}')
			
			if isinstance(check, (dict, list)):
				checkStructure(check, item, item_path)
	
	return content


def hideEmail(email: str) -> str:
	"""
	Converts most characters of the email into * to hide it
	"""

	domain = email[email.find('@')+1:] # Get domain part of email

	# Get characters
	firstChar = email[0]
	lastChar = email[email.find('@')-1]

	firstDomainChar = domain[0]
	lastDomainChar = domain[-1]

	# Return hidden
	return f'{firstChar}*******{lastChar}@{firstDomainChar}***{lastDomainChar}'


def saltPassword(password: str, email: str) -> str:
	"""
	Salt the password and return the salted password
	"""

	return password + email + current_app.config['RANDOM_SALT']


def checkPasswordFormat(password: str) -> bool:
	"""
	Determine if password meets password conditions

	Conditions:
	- More than 8 characters long
	- Mix of numbers, symbols, letters
	- Letters include both capital and lower-case
	"""

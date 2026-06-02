from app.models.database import db
from app.utils import hash, hideEmail, saltPassword
from app.utils.exceptions import EmailAlreadyRegistered


# Determine if user credentials match database
def checkLogin(email: str, password: str) -> str | None:
	"""
	Determine if the user credentials match the database for login.
	Returns UID if true, otherwise returns None
	"""

	# Check DB for credentials
	user = db().fetch(f"""
			SELECT id FROM users 
			WHERE email='{hash(email)}' AND password='{hash(saltPassword(password, email))}';
		""")
	
	# Check if exists
	if len(user) == 0:
		return None
	else:
		return user[0][0] # Returns ID


# Create user
def registerUser(name: str, email: str, password: str) -> str:
	"""
	Register a user to the database and request OTP be sent.
	This doesn't send OTP but OTP code needs to be generated before this runs

	Returns UUID
	"""

	# Determine if email already registered
	registered = db().fetch(f"""
		SELECT id FROM users
		WHERE email='{hash(email)}';				 
	""")

	if len(registered) != 0:
		raise EmailAlreadyRegistered()
	
	# Register user to database
	db().modify(f"""
		INSERT INTO users (name, email_hidden, email_hash, pass)
		VALUES (
					'{name}',
					'{hideEmail(email)}',
					'{hash(email)}',
					'{hash(saltPassword(password, email))}'
			 	);
	""")


# Confirm email is validated
def validateEmail(uuid: str) -> None:
	"""
	Set/Confirm that the user's email has been validated in the database
	"""

	db().fetch(f"""
		UPDATE users 
		SET email_validated = 'true' 
		WHERE id='{uuid}';
	""")

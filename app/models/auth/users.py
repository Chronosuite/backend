from app.models.database import db
from app.utils import hash, Emailer


# Determine if user credentials match database
def checkLogin(email: str, password: str) -> str | None:
	"""
	Determine if the user credentials match the database for login.
	Returns UID if true, otherwise returns None
	"""

	# Check DB for credentials
	user = db().fetch(f"""
			SELECT id FROM users 
			WHERE email='{email}' AND password='{password}';
		""")
	
	# Check if exists
	if len(user) == 0:
		return None
	else:
		return user[0][0] # Returns ID

from app.models.database import db
from app.utils import hash
from app.utils.exceptions import ExpiredSession, NeedOTP


# Create new login session
def createSession(agent: str, uid: str) -> str:
	"""
	Create a new login session
	"""

	# Refresh old sessions
	delOldSession()

	# Create session
	id = db().modifyAndReturn(f"""
		INSERT INTO sessions (user, agent)
		VALUES ('{uid}', '{hash(agent)}')
		RETURNING id;
	""")[0]

	return id


# Retrieve info about session
def getSession(sessID: str) -> dict | None:
	"""
	Return user info about session given id

	Returns it in dictionary format:
	userInfo = {
		'id'
		'name'
		'email'
		'plan'
		'planDate'
		'date'
	}
	"""

	# Refresh old sessions
	delOldSession()

	# Fetch info
	uid = db().fetch(f"""
		SELECT user FROM sessions
		WHERE (id='{sessID}');
	""")

	# Check if session exists
	if len(uid) == 0:
		raise ExpiredSession()
	
	# Get user info
	user = db().fetch(f"""
		SELECT id, name, email_hidden, email_verified, plan, plan_date, created FROM users
		WHERE (id='{uid[0][0]}');
	""")

	# Determine if need OTP code/email verification
	if str(user[3]).lower() == 'true':
		raise NeedOTP()

	# Process data
	userInfo = {
		'id': user[0],
		'name': user[1],
		'email': user[2],
		'plan': user[4],
		'planDate': user[5],
		'date': user[6]
	}

	return userInfo


# Delete old sessions
def delOldSession() -> None:
	"""
	Delete expired sessions
	"""

	db().modify("""
		DELETE FROM sessions
		WHERE created < NOW() - INTERVAL '30 days';
	""")

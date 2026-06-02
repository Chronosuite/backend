from app.models.database import db
from app.utils import hash
from app.utils.exceptions import ExpiredSession, NeedOTP


# Create new login session
def createSession(agent: str, uid: str, needOTP: bool = False) -> str:
	"""
	Create a new login session
	"""

	# Refresh old sessions
	delOldSession()

	# Create session
	id = db().modifyAndReturn(f"""
		INSERT INTO sessions (user, agent, need_otp),
		VALUES ('{uid}', '{hash(agent)}', '{str(needOTP).lower()}')
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
		SELECT user, need_otp FROM sessions
		WHERE (id='{sessID}');
	""")

	# Check if session exists
	if len(uid) == 0:
		raise ExpiredSession()
	
	# Determine if need OTP code
	elif str(uid[0][1]).lower() == 'true':
		raise NeedOTP()

	# Get user info
	user = db().fetch(f"""
		SELECT id, name, email_hidden, plan, plan_date, created FROM users
		WHERE (id='{uid[0][0]}');
	""")

	# Process data
	userInfo = {
		'id': user[0],
		'name': user[1],
		'email': user[2],
		'plan': user[3],
		'planDate': user[4],
		'date': user[5]
	}

	return userInfo


# OTP Confirm Session
def confirmSession(sessID: str) -> None:
	"""
	Set the need_otp property to False for a sessionID
	"""

	db().modify(f"""
		UPDATE sessions
		SET need_otp = 'true'
		WHERE id='{sessID}';
	""")


# Delete old sessions
def delOldSession() -> None:
	"""
	Delete expired sessions
	"""

	db().modify("""
		DELETE FROM sessions
		WHERE created < NOW() - INTERVAL '30 days';
	""")

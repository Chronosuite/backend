from app.models.database import db
from app.utils import hash


# Create new login session
def createSession(agent: str, uid: str) -> str:
	"""
	Create a new login session
	"""

	id = db().modifyAndReturn(f"""
		INSERT INTO sessions (user, agent),
		VALUES ({uid}, {hash(agent)})
		RETURNING id;
	""")[0]

	return id


# Retrieve info about session
def getSession(sessID: str) -> dict | None:
	"""
	Return user info about session given id
	"""

	uid = db().fetch(f"""
			SELECT user FROM sessions
			WHERE (id={sessID});
		""")

	user = db().fetch(f"""
		SELECT id, name, email_hidden, plan, plan_date, created FROM users
		WHERE (id={uid});
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

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

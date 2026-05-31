from app.models.database import db
from app.utils import hash, Emailer


# Send OTP Code
def sendCode(uuid: str, email: str, name: str) -> None:
	"""
	Send One-Time Password to given email
	"""



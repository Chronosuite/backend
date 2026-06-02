from flask import jsonify, request

from app.routes.routeManager import RouteManager
from app.models.auth import users, sessions
from app.utils import checkStructure
from app.utils.exceptions import RequestBodyException

account = RouteManager().auth


@account.post('/login')
def login() -> None:
	"""
	Method to login to account
	"""

	# Process Request
	SAMPLE_REQUEST_DATA = {
		'email': 'example@gmail.com',
		'pass': 'password hash' # Hashed client-side
	}

	# Parse request
	try:
		body = checkStructure(SAMPLE_REQUEST_DATA, request.get_json())
	except RequestBodyException as e: # If error with parsing data then return error
		return jsonify({
				'status': 'error',
				'message': str(e)
			}), 422 # Unprocessable entity status code

	# Retrieve + Hash Email
	usrPass = body['pass']
	usrEmail = hash(body['email'])

	# Get user agent
	agent = request.headers.get('User-Agent')

	# Check credentials
	uid = users.checkLogin(usrEmail, usrPass)

	if uid != None:
		# Create session
		sessID = sessions.createSession(agent, uid)
	else:
		# Return failed to login error
		return jsonify({
				'status': 'error',
				'message': 'Login credentials incorrect.'
			}), 401
	
	# Return session ID
	return jsonify({
			'status': 'success',
			'session': sessID
		}), 200

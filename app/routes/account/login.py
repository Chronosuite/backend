from flask import jsonify, request

from app.routes.routeManager import RouteManager
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
		'pass': 'password hash'
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

	#

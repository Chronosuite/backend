from brevo import Brevo
from flask import current_app


class Emailer:
	_instance = None

	def __new__(cls, *args, **kwargs):
		"""Ensure only one instance of the class is created (Singleton)."""
		
		if not cls._instance:
			cls._instance = super(Emailer, cls).__new__(cls, *args, **kwargs)
		
		return cls._instance
	

	def __init__(self) -> None:
		"""Initialize the email brevo client connection if it doesn't already exist."""
		
		if not hasattr(self, "_client"):
			key = current_app.config["BREVO_KEY"]
			self.email = current_app.config["BREVO_EMAIL"]
			self.name = current_app.config["BREVO_NAME"]

			self._client = Brevo(api_key=key)

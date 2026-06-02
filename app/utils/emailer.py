from brevo import Brevo
from brevo.transactional_emails import (
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem,
)
from flask import current_app

from app.utils.exceptions import FailedEmail


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


	def sendEmail(self, name: str, recipient: str, subj: str, content: str) -> None:
		"""
		Send email from the configured Brevo client to the recipient given the relevant info
		"""

		try:
			self._client.transactional_emails.send_transac_email(
				html_content=content,

				sender=SendTransacEmailRequestSender(
					email=self.email,
					name=self.name,
				),

				subject=subj,
				
				to=[
					SendTransacEmailRequestToItem(
						email=recipient,
						name=name,
					)
				],
			)
			
		except Exception as e:
			raise FailedEmail(str(e))

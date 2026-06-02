from datetime import datetime


class Event:
	def __init__(self, 
				name: str, 
				desc: str, 
				calID: str, 
				startTime: datetime, 
				endTime: datetime, 
				allDay: bool,
				created: datetime) -> None:
		"""
		Model class for an event
		"""

		# Set attributes
		self.name: str = name
		self.desc: str = desc
		self.calID: str = calID
		self.startTime: datetime = startTime
		self.endTime: datetime = endTime
		self.allDay = allDay
		self.created: datetime = created

		# Set attributes to be set later
		self.attendees: list[str] = []

from datetime import datetime


class Event:
	def __init__(self, 
			  	id: int,
				name: str, 
				desc: str, 
				startTime: datetime, 
				endTime: datetime, 
				allDay: bool,
				calID: str | None = None, 
				linkedTaskID: str | None = None) -> None:
		"""
		Model class for an event
		"""

		# Set attributes
		self.id: int = id
		self.name: str = name
		self.desc: str = desc
		self.startTime: datetime = startTime
		self.endTime: datetime = endTime
		self.allDay: bool = allDay
		self.calID: str | None = calID
		self.linkedTaskID: str | None = linkedTaskID

		# Set attributes to be set later
		self.attendees: list[str] = []

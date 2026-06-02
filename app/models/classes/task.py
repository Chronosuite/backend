from datetime import datetime

from app.models.classes.event import Event


class Task:
	def __init__(self, 
			  	id: int,
				name: str, 
				desc: str, 
				categoryID: str, 
				deadline: datetime, 
				allDay: bool,
				parentTask: 'Task' = None) -> None:
		"""
		Model class for a task
		"""

		# Set attributes
		self.id: int = id
		self.name: str = name
		self.desc: str = desc
		self.categoryID: str = categoryID
		self.deadline: datetime = deadline
		self.allDay: bool = allDay
		self.parentTask: 'Task' = parentTask

		# Set attributes to be set later
		self.taskEvents: list[int] = [] # Links to IDs

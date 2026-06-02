from datetime import datetime


class Task:
	def __init__(self, 
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
		self.name: str = name
		self.desc: str = desc
		self.categoryID: str = categoryID
		self.allDay: bool = allDay
		self.parentTask: 'Task' = parentTask

		# Set attributes to be set later
		self.taskE
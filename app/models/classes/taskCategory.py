from app.models.classes.task import Task


class TaskCategory:
	def __init__(self, id: int, label: str, ownerID: str, color: str, archived: bool) -> None:
		"""
		Model class to represent a task category
		"""

		# Set base attributes
		self.id: int = id
		self.label: str = label
		self.ownerID: str = ownerID
		self.color: str = color
		self.archived: bool = archived

		# Set default attributes to be changed later
		self.tasks: list[Task] = []

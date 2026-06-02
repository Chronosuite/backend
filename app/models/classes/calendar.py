class Calendar:
	def __init__(self, id: int, name: str, ownerID: str, color: str) -> None:
		"""
		Model class to represent a calendar
		"""

		# Set base attributes
		self.id: int = id
		self.name: str = name
		self.ownerID: str = ownerID
		self.color: str = color

		# Set default attributes to be changed later
		self.events: list[int] = [] # List of IDs
		self.members: list[str] = [] # links to UUID of users

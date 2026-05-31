from flask import Blueprint, Flask
from flask_cors import CORS


class RouteManager:
	_instance = None

	BLUEPRINTS = (
		'account',
		'calendar',
		'tasks'
	) 

	def __new__(cls, *args, **kwargs):
		"""Ensure only one instance of the class is created (Singleton)."""
		
		if not cls._instance:
			cls._instance = super(RouteManager, cls).__new__(cls, *args, **kwargs)
		
		return cls._instance
	

	def __init__(self) -> None:
		"""Initialize the Routes class if it doesn't already exist."""
		
		if not hasattr(self, "index"):
			self.index = Flask(__name__)

			CORS(self.index, resources={
				r"/*": {"origins": "*"}
			})

			# Load configuration
			self.index.config.from_object('config.Config')

			# Set up blueprints
			self.search = Blueprint('search', __name__, url_prefix='/search') # Search Route
			self.share = Blueprint('share', __name__, url_prefix='/share') # Share Route


	def registerBlueprints(self) -> None:
		"""Register blueprints once defined"""
		
		# Automatically register blueprints
		for blueprint in self.BLUEPRINTS:
			self.index.register_blueprint(self.__getattribute__(blueprint))

		# Output URL configuration for debug
		print('Configured URL Map:')
		print(self.index.url_map)

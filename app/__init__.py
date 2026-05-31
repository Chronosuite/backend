# Import routes
from app.routes import *


# Create app
def createApp():
	RouteManager().registerBlueprints()

	# Return main route
	return RouteManager().index

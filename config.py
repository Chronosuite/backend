from os import getenv

# Get environment variables
POSTGRES_USER = getenv('POSTGRES_USER', '')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', '')
POSTGRES_DB = getenv('POSTGRES_DB', '')
	# Other
	FORCE_RESTART_SQL = False

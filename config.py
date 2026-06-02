from os import getenv

class Config:
	# Get environment variables

	# PostGreSQL
	DB_USER = getenv('POSTGRES_USER', '')
	DB_PASS = getenv('POSTGRES_PASSWORD', '')
	DB_NAME = getenv('POSTGRES_DB', '')
	DB_HOST = getenv('POSTGRES_HOST', '')
	DB_PORT = getenv('POSTGRES_PORT', '')

	DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


	# Email Settings
	BREVO_EMAIL = getenv('BREVO_EMAIL', '')
	BREVO_KEY = getenv('BREVO_API_KEY', '')

	BREVO_NAME = 'No-Reply'


	# Security
	RANDOM_SALT = getenv('RANDOM_SALT', 'please_set_this')


	# Other
	FORCE_RESTART_SQL = False
	ASSETS_FOLDER = './assets'

	FRONTEND_URL = 'https://chronosuite.net'

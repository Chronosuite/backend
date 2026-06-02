import psycopg2
from urllib.parse import urlparse
from flask import current_app


class db:
	_instance = None

	def __new__(cls, *args, **kwargs):
		"""Ensure only one instance of the class is created (Singleton)."""
		
		if not cls._instance:
			cls._instance = super(db, cls).__new__(cls, *args, **kwargs)
		
		return cls._instance
	

	def __init__(self) -> None:
		"""Initialize the database connection pool if it doesn't already exist."""
		
		if not hasattr(self, "_pool"):
			database_url = current_app.config["DATABASE_URL"]
			parsed_url = urlparse(database_url)

			self._pool = psycopg2.pool.SimpleConnectionPool(
				minconn=1,
				maxconn=10,
				user=parsed_url.username,
				password=parsed_url.password,
				host=parsed_url.hostname,
				port=parsed_url.port,
				database=parsed_url.path.lstrip("/"),
			)

			# Init DB
			self.initializeDB()


	def get_connection(self):
		"""Get a connection from the pool."""
		return self._pool.getconn()


	def release_connection(self, conn):
		"""Release a connection back to the pool."""
		self._pool.putconn(conn)


	def close_all_connections(self):
		"""Close all connections in the pool."""
		self._pool.closeall()

	
	def fetch(self, query: str) -> list[list]:
		"""Execute a query which involves fetching results"""

		conn = self.get_connection()
		cursor = conn.cursor()

		cursor.execute(query)

		result = cursor.fetchall()

		cursor.close()
		self.release_connection(conn)

		return result
	
	
	def modify(self, query: str) -> None:
		""" For insert/delete statements where no result is returned but the db is changed """

		conn = self.get_connection()
		cursor = conn.cursor()

		cursor.execute(query)
		conn.commit()

		cursor.close()
		self.release_connection(conn)


	def modifyAndReturn(self, query: str) -> list:
		"""For insert and allows for return"""

		conn = self.get_connection()
		cursor = conn.cursor()

		cursor.execute(query)
		conn.commit()

		result = cursor.fetchone()
		
		cursor.close()
		self.release_connection(conn)

		return result



	# Set up DB
	def initializeDB(self) -> None:
		"""
		Set up tables and whatnot in SQL table if they don't exist
		"""

		# Create tables
		def createTable(name, contents) -> None:
			# Determine if need to force restart/recreate database tables
			if current_app.config["FORCE_RESTART_SQL"]:
				db.modify(f"DROP TABLE IF EXISTS {name};")
				db.modify(f"CREATE TABLE {name} ({contents});")
			else:
				db.modify(f"CREATE TABLE IF NOT EXISTS {name} ({contents});")


		# User Tables
		createTable('users', """
				id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
				name VARCHAR(3000) NOT NULL,
			  	email_hidden CHAR(15) NOT NULL,
				email_hash CHAR(64) NOT NULL,
				pass CHAR(64) NOT NULL,
				plan VARCHAR(9) CHECK (plan IN ('init', 'free', 'trial', 'pro', 'unlimited')) NOT NULL DEFAULT 'free',
				plan_date TIMESTAMP NOT NULL DEFAULT NOW(),
			  	created TIMESTAMP NOT NULL DEFAULT NOW()
			""")


		# Calendar Tables
		createTable('cal', """
				id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
				owner UUID REFERENCES users(id) ON DELETE CASCADE
			""") # For calendar
		
		createTable('cal_events', """
				id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
				email VARCHAR(254) NOT NULL
			""") # For events


		# Tasks Tables
		createTable('tasks', """
				id SERIAL PRIMARY KEY,
			  	name VARCHAR(5000) NOT NULL,
			  	descr VARCHAR(100000) NOT NULL,
			  	category INT REFERENCES tasks_categories(id) ON DELETE CASCADE
			""")
		
		createTable('tasks_categories', """
				id SERIAL PRIMARY KEY,
				label VARCHAR(2500) NOT NULL,
			  	color CHAR(6) NOT NULL,
			  	owner UUID REFERENCES users(id) ON DELETE CASCADE
			""")
		

		# Share/Many-To-Many Tables
		createTable('tasks_share', """
				id SERIAL PRIMARY KEY,
			  	tasks INT REFERENCES cal(id) ON DELETE CASCADE,
			  	user UUID REFERENCES users(id) ON DELETE CASCADE
			""")
		
		createTable('tasks_categories_share', """
				id SERIAL PRIMARY KEY,
			  	category INT REFERENCES tasks_categories(id) ON DELETE CASCADE,
			  	user UUID REFERENCES users(id) ON DELETE CASCADE
			""")
		
		createTable('cal_share', """
				id SERIAL PRIMARY KEY,
			  	calendar INT REFERENCES cal(id) ON DELETE CASCADE,
			  	user UUID REFERENCES users(id) ON DELETE CASCADE
			""")
		
		createTable('cal_events_share', """
				id SERIAL PRIMARY KEY,
			  	event INT REFERENCES cal_events(id) ON DELETE CASCADE,
			  	user UUID REFERENCES users(id) ON DELETE CASCADE
			""")


		# OTP Codes
		createTable('otp_codes', """
				id SERIAL PRIMARY KEY,
				code_num CHAR(64) NOT NULL,
				user UUID REFERENCES users(id) ON DELETE CASCADE,
				created TIMESTAMP NOT NULL DEFAULT NOW()
			""")


		# Session/Auth Tables
		createTable('sessions', """
				id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
				user UUID REFERENCES users(id) ON DELETE CASCADE,
			  	agent CHAR(64) NOT NULL,
			  	need_otp BOOLEAN NOT NULL DEFAULT false,
				created TIMESTAMP NOT NULL DEFAULT NOW()
			""")

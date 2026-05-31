import psycopg2
from psycopg2 import pool
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

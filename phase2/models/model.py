from pymongo import MongoClient
import os

class Model:
	def __init__(self, port):
		"""
		Sets up the connection and cursor for any of the children models to use
		"""

		# Validates that the port given is a valid, existing db
		self.client = MongoClient('mongodb://localhost:'+port)
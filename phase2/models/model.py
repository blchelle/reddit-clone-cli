from pymongo import MongoClient
import sys

class Model:
	def __init__(self, port):
		"""
		Sets up the connection and cursor for any of the children models to use
		"""

		self.client = MongoClient('mongodb://localhost:'+port)
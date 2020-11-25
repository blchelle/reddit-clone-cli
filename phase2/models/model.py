from pymongo import MongoClient
import sys

class Model:
	def __init__(self, port):
		"""
		Sets up the connection and cursor for any of the children models to use
		"""

		# Validates that the port given is a valid, existing db
		try:
			print('Trying to connect...')
			self.client = MongoClient('mongodb://localhost:'+port, serverSelectionTimeoutMS=5000)
			self.client.server_info()
			print('Successfully connected to db at port ' + port)
		except:
			# do whatever you need
			print('No MongoDB Server Available at Port ' + port)
			print('Exiting...')
			sys.exit(-1)

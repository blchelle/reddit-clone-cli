from models import model
from datetime import datetime
import uuid
import sqlite3

class PostsModel(model.Model):
	dbname = '291db'
	def updateQuestionView(self, pid):
		"""
		Updates view count for selected question

		"""
		db = self.client[self.dbname]
		posts = db["Posts"]
		buffer = posts.find({"Id":pid})

		newCount = int(buffer[0]["ViewCount"]) + 1
		posts.update({"Id":pid},{"$set":{"ViewCount":str(newCount)}})


	def createAnswer(self, title, body, qid, uid):
		"""
		Inserts a post into the posts table and the answers table

		This implemented as a transaction since we don't want one insert to succeed
		while the other insert fails

		Parameters
		----------
		title : str
			The title of the answer post
		body : str
			The body of the answer post
		qid : str
			The pid of the question which the post is answering
		uid : str
			The uid of the user creating the answer

		Returns
		-------
		bool
			True if the answer was successfully inserted into both tables
			False if there was an error at either step
		"""

		db = self.client["291db"]
		posts = db["Posts"]
		latestID=1
		latestIDs = posts.find().sort([("$natural",-1)]).limit(1)
		for doc in latestIDs:
			latestID = doc["Id"]
		
		newID = int(latestID)+1

		posts.insert({
			"Id":str(newID),
			"PostTypeId": "2",
			"ParentId": qid,
			"CreationDate":str(datetime.now()),
			"Title": title,
			"Body": "<p>"+body+"</p>\n",
			"OwnerUserId": uid,
			"Score": 0,
			"CommentCount": 0,
			"ContentLicense": "CC BY-SA 2.5"
			})

		return True
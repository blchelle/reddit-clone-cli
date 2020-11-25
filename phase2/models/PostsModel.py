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


	def listAnswersForQuestion(self, pid):
		"""
		Lists all the answers to a question with pid.

		Args:
			pid: The id field of the question post

		Returns:
			list(dict): All the answers for the question
		"""

		# Gets the posts collection
		db = self.client[self.dbname]
		posts = db["Posts"]

		# Queries for all answer that answer the question
		results = []
		results.extend(posts.find(
			{
				'$and':
					[
						{ "ParentId": pid },
						{ "PostTypeId": "2" }
					]
			},
			{
				"Id": 1,
				"Body": 1,
				"CreationDate": 1,
				"Score": 1
			}
		))

		return results


	def getAnswerFromPid(self, pid):
		"""
		Gets all the fields for a document from the posts collection
		This method should be called within the context of getting the info
		form an answer

		Args:
			pid: The pid of the answer post

		Return:
			dict: All the fields for the answer post
		"""
		# Gets the posts collection
		db = self.client[self.dbname]
		posts = db["Posts"]

		# Queries for all answer that answer the question
		result = posts.find_one( { "Id": pid } )

		return result

	def getAcceptedAnswerId(self, qid):
		"""
		Gets the pid of the accepted answer for a qid, or None if there isn't one

		Args:
			qid: The pid of the answer post

		Return:
			str: The id of the accepted answer
		"""
		# Gets the posts collection
		db = self.client[self.dbname]
		posts = db["Posts"]

		# Queries for the accepted answer id
		result = posts.find_one(
			{
				"$and":
					[
						{ "AcceptedAnswerId": { "$exists": 1 } },
						{ "Id": qid }
					]
			},
			{
				"AcceptedAnswerId": 1
			}
		)

		if result is None:
			return None
		else:
			return result['AcceptedAnswerId']


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

	def userHasVotedOnPost(self, uid, pid):
		"""
		Determines if a user (uid) has voted on the post (pid)

		Args:
			uid: The id of the user
			pid: The id of the post

		Returns:
			bool: True if the user has voted on the post, false otherwise
		"""

		db = self.client["291db"]
		votes = db["Votes"]

		result = votes.find_one( { "$and": [ { "UserId": uid }, { "PostId": pid } ] } )

		return result is not None

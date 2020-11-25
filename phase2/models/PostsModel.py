from models import model
from datetime import datetime

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


	def getPostsFromPid(self, pid):
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


	def createAnswer(self, body, qid, uid):
		"""
		Inserts a answers document into the posts table

		Args:
			body : str
				The body of the answer post
			qid : str
				The pid of the question which the post is answering
			uid : str
				The uid of the user creating the answer

		Return:
			bool:
				True if the answer was successfully inserted into both tables
				False if there was an error at either step
		"""

		db = self.client["291db"]
		posts = db["Posts"]
		latestID = 1
		latestIDs = posts.find().sort([("$natural",-1)]).limit(1)
		latestID = latestIDs[0]["Id"]

		newID = int(latestID) + 1

		documentFields = {
			"Id":             str(newID),
			"PostTypeId":     "2",
			"ParentId":       qid,
			"CreationDate":   str(datetime.now().isoformat())[0:-3],
			"Body":           body,
			"Score":          0,
			"CommentCount":   0,
			"ContentLicense": "CC BY-SA 2.5"
		}

		if uid != -1:
			documentFields.update( { "OwnerUserId": uid } )

		posts.insert(documentFields)

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


	def addVoteToPost(self, pid, uid):
		"""
		Adds a row to the votes table for the post and user specified

		Parameters
		----------
		pid : str
			The pid of the post being voted on
		uid : str
			The uid of the user giving the vote
		"""

		db = self.client["291db"]
		votes = db["Votes"]
		posts = db["Posts"]
		latestID = 1
		latestIDs = votes.find().sort([("$natural",-1)]).limit(1)

		latestID = latestIDs[0]["Id"]

		newID = int(latestID) + 1
		documentFields = {
			"Id":             str(newID),
			"PostId":		  pid,
			"VoteTypeId":     "2",
			"CreationDate":   str(datetime.now().isoformat())[0:-3]
		}

		if uid != -1:
			documentFields.update( { 'UserId': uid } )

		votes.insert(documentFields)

		buffer = posts.find({"Id":pid})

		newScore = int(buffer[0]["Score"]) + 1
		posts.update({"Id":pid},{"$set":{"Score":str(newScore)}})

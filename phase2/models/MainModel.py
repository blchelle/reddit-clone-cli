from models import model
from datetime import datetime
import uuid
import sqlite3
import re

class MainModel(model.Model):

	def postQuestion(self, title, body, tagsList, poster):
		"""
		inserts question posts into the database


		Parameters
		----------
		title : str
			title of question
		body : str
			body of question
		poster: str
			username of poster

		Return
		----------
		None or {}

		"""

		db = self.client["291db"]
		posts = db["Posts"]
		tags_collection = db["Tags"]
		latestID=0
		latestIDs = posts.find().sort([("$natural",-1)]).limit(1)
		for doc in latestIDs:
			latestID = doc["Id"]

		newID = int(latestID)+1

		tags =""

		for tag in tagsList:

			tag_exist = tags_collection.find( { "TagName": tag } )
			if(tag_exist.count() != 0):
				for doc in tag_exist:
					tags_collection.update_one(
						{
							"_id": doc["_id"]
						},
						{
							"$set": { "Count": doc["Count"] + 1 }
						}
					)
			else:
				latestTagID=0
				latestTagIDs = tags_collection.find().sort( [ ( "$natural", -1) ] ).limit(1)

				for doc in latestTagIDs:
					latestTagID = doc["Id"]
				newTagID = int(latestTagID)+1

				tags_collection.insert(
					{
						"Id": str(newTagID),
						"TagName": tag,
						"Count": 1
					}
				)


			tags+="<"+tag+">"

		documentFields = {
			"Id":str(newID),
			"PostTypeId": "1",
			"CreationDate":str(datetime.now().isoformat()),
			"Title": title,
			"Body":body,
			"Tags": tags,
			"Score": 0,
			"ViewCount": 0,
			"AnswerCount": 0,
			"CommentCount": 0,
			"FavoriteCount": 0,
			"ContentLicense": "CC BY-SA 2.5"
		}

		if poster != -1:
			documentFields.update( { 'OwnerUserId': poster } )

		posts.insert(documentFields)


	test="test"
	dbname = "291db"
	def findQuestions(self, searchString):
		"""
		find questions based on keywords

		Returns
		-------
		list of matching questions

		"""
		searchExpr = searchString.split(" ")
		patternList=[]
		results = []
		for keyWord in searchExpr:
			pattern = re.compile(".*" + keyWord + ".*", re.IGNORECASE)
			patternList.append(pattern)
		db = self.client[self.dbname]
		posts = db["Posts"]
		buffer = posts.find(
			{
				"PostTypeId":"1",
				'$or':
				[
					{ "Title": { '$in': patternList } },
					{ "Body":  { '$in': patternList } },
					{ "Tags":  { '$in': patternList } }
				]
			}
		)

		results.extend(buffer)
		return results

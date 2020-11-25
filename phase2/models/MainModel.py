from models import model
from datetime import datetime
import uuid
import sqlite3
import re
import json

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
		latestID = latestIDs[0]["Id"]

		newID = int(latestID)+1
		
		bodyTerms = []
		titleTerms = []

		if(body is not None):
			bodyTerms = set(re.split('[^a-zA-Z0-9]', body.lower()))

		if(title is not None):
			titleTerms = set(re.split('[^a-zA-Z0-9]', title.lower()))

		# Joins the set of terms
		terms = bodyTerms.union(titleTerms)
		copyTerms = terms.copy()

		# Filters out all terms of length less than 3
		for term in copyTerms:
			if len(term) < 3:
				terms.remove(term)

		tags =""

		for tag in tagsList:

			tag_exist = tags_collection.find( { "TagName": tag } )
			if(tag_exist.count() != 0):
				tags_collection.update_one(
					{
						"_id": tag_exist[0]["_id"]
					},
					{
						"$set": { "Count": tag_exist[0]["Count"] + 1 }
					}
				)
			else:
				latestTagID=0
				latestTagIDs = tags_collection.find().sort( [ ( "$natural", -1) ] ).limit(1)
				latestTagID = latestTagIDs[0]["Id"]
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
			"Id":             str(newID),
			"PostTypeId":     "1",
			"CreationDate":   str(datetime.now().isoformat())[0:-3],
			"Title":          title,
			"Body":           body,
			"Tags":           tags,
			"Terms":		  tuple(terms),
			"Score":          0,
			"ViewCount":      0,
			"AnswerCount":    0,
			"CommentCount":   0,
			"FavoriteCount":  0,
			"ContentLicense": "CC BY-SA 2.5"
		}

		if poster != -1:
			documentFields.update( { 'OwnerUserId': poster } )

		posts.insert(documentFields)
		posts.create_index('Terms')


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

		useIndexSearch = True
		for keyWord in searchExpr:
			if len(keyWord)<3:
				useIndexSearch = False
		for keyWord in searchExpr:
			if useIndexSearch:
				pattern = (keyWord).lower()
				db = self.client[self.dbname]
				posts = db["Posts"]

				buffer = posts.find({"PostTypeId":"1", "Terms":pattern})

				for p in buffer:
					if p not in results:
						results.append(p)

			else:
				break


		if useIndexSearch:

			return (results)

		db = self.client[self.dbname]
		posts = db["Posts"]
		buffer = posts.find({"PostTypeId":"1", '$or':[
		{"Title":{'$in': patternList}},
		{"Body":{'$in': patternList}},
		{"Tags":{'$in': patternList}}]})
		results.extend(buffer)
		return results


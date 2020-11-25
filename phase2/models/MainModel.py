from models import model
from datetime import datetime
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

		tagsSet =set()
		tags =""

		for tag in tagsList:

			if(tag not in tagsSet):
				tagsSet.add(tag)
				tags+="<"+tag+">"

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
		db = self.client[self.dbname]
		posts = db["Posts"]

		searchExpr = searchString.split(" ")
		results = set([])

		for keyword in searchExpr:
			if len(keyword) >= 3:
				keywordSearchResult = posts.find(
					{
						"PostTypeId":"1", "Terms": keyword.lower()
					}
				)
			else:
				regexPattern = re.compile('.* ' + keyword + ' .*', re.IGNORECASE)

				keywordSearchResult = posts.find(
					{
						"PostTypeId":"1",
						'$or':
						[
							{ "Title": { '$regex': regexPattern } },
							{ "Body":  { '$regex': regexPattern } },
							{ "Tags":  { '$regex': regexPattern } }
						]
					}
				)

			for post in keywordSearchResult:
				# Convert the post to a string so we can put it into a set
				postString = ''

				id           = post['Id']
				title        = post['Title']
				creationDate = post['CreationDate']
				score        = str(post['Score'])
				numAnswers   = str(post['AnswerCount'])

				postString += id + (7 - len(id)) * ' '

				if len(title) > 80:
					postString += title[0:80] + "... "
				else:
					postString += title[0:len(title)] + ((84 - len(title)) * " ")

				postString += creationDate + ' '
				postString += score + (7 - len(score)) * ' '
				postString += numAnswers

				results.add(postString)

		results = list(results)
		results.sort(key=lambda id: int(id.split()[0]))
		return results

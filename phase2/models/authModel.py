from models import model
import sqlite3


class AuthModel(model.Model):

	def attemptLogin(self, uid):
		"""
		Checks the users table to find a match of the username
		and password
		Parameters
		----------
		uid : str
				The uid given at the command-line
		password : str
				The password given at the command-line
		Return
		----------
		None or {}
				The result of the login query
				Return will be none if no such user is found
				Otherwise, the return will be the users information
		"""

		# Template query for checking if the user is logged in

		results = {}

		db = self.client["291db"]
		posts = db["Posts"]
		votes = db["Votes"]

		p_results = posts.find({"OwnerUserId": uid})

		if(p_results.count()==0):
				return results

		q_results = posts.aggregate([{"$match": {"OwnerUserId": uid}}, {"$match": {"PostTypeId": "1"}}, {
									"$group": {"_id": "$OwnerUserId", "avgScoreQ": {"$avg": "$Score"}, "noOfQuestions": {"$sum": 1}}}])
		a_results = posts.aggregate([{"$match": {"OwnerUserId": uid}}, {"$match": {"PostTypeId": "2"}}, {
									"$group": {"_id": "$OwnerUserId", "avgScoreA": {"$avg": "$Score"}, "noOfAnswers": {"$sum": 1}}}])

		p_results = posts.find({"OwnerUserId": uid})
		postList = []
		for r in p_results:
			postList.append(r["Id"])

		v_results = votes.find({"PostId": {"$in": postList}})

		for r in q_results:
			results["noQ"] = str(r["noOfQuestions"])
			results["avgSQ"] = str(r["avgScoreQ"])

		for r in a_results:
			results["noA"] = str(r["noOfAnswers"])
			results["avgSA"] = str(r["avgScoreA"])

		results["votes"] = str(v_results.count())

		return results

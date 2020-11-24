"""This module brings the cli module."""
from views import view
from PyInquirer import style_from_dict, Token, prompt, Separator
import pprint


class AuthView(view.View):

	def getAuthenticationAction(self):
		"""
		Asks the user how they'd like to authenticate and returns the result
		Returns
		-------
		'Login with Username' or 'Login as anon' or 'Exit'
		"""

		options = [
			{
				'type': 'list',
				'message': 'Select an action',
						'name': 'auth method',
						'choices': [
								"Login with UserId",
								"Login as Anonymous",
								"Exit"
						]
			}
		]

		return prompt(options, style=self.style)

	def getLoginCredentials(self):
		"""
		Prompts the user to enter their credentials and returns the result
		Returns
		-------
		{}
				The users entered login credentials
		"""

		loginPrompts = [
			{
				'type': 'input',
				'message': 'Enter your uid:',
				'name': 'uid'
			}
		]

		uid = ''
		while uid == '':
			uid = prompt(loginPrompts, style=self.style)['uid'].strip()

			if uid == '':
				self.logMessage('# ERROR: Please provide a non-empty uid')

		return uid


	def displayReport(self, uid, results):

		print()
		print("Report for User: "+uid)
		print()

		if("noQ" in results):
			print("Number of Questions Posted  : " + results["noQ"])
		else:
			print("Number of Questions Posted  : None")

		if("avgSQ" in results):
			print("Average Score for Questions : " + results["avgSQ"])
		else:
			print("Average Score for Questions : None")

		if("noA" in results):
			print("Number of Answers Posted    : " + results["noA"])
		else:
			print("Number of Answers Posted    : None")

		if("avgSA" in results):
			print("Average Score for Answers   : " + results["avgSA"])
		else:
			print("Average Score for Answers   : None")

		if("votes" in results):
			print("Votes received by User      : " + results["votes"])
		else:
			print("Votes received by User      : None")

		print()

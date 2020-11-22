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
					"Login with Username",
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

		return prompt(loginPrompts, style=self.style)

	def displayReport(self,uid,results):

		print("Report for User: "+uid)
		print()
		for m in results:
			pp = pprint.PrettyPrinter(indent=4)
			pp.pprint(m)
			print()
			print()

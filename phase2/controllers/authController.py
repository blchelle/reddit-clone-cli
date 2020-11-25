"""
Phase 2 of the Reddit Clone CLI.
Authentication Controller

This file is responsible for ensuring clean communication between the
cli for authentication (AuthView) and the db (AuthModel)

Contributors:
    Alireza Azimi
    Archit Siby
    Brock Chelle
"""
from models import authModel
from views import authView
from controllers import MainController

class AuthController:
	def __init__(self, port):
		self.model = authModel.AuthModel(port)
		self.view = authView.AuthView()
		self.port = port

	def run(self):
		"""
		Runs through the authentication process
		"""
		while True:
			# Prompts and retrieves the users auth choice
			authAction = self.view.getAuthenticationAction()
			if authAction == {}:
				self.view.logMessage("#ERROR: Don't Click on the Options, Try again with keystrokes")
				continue

			authAction = authAction['auth method']

			if authAction == 'Login with UserId':
				# Prompts and retrieves the users credentials
				uid = self.view.getLoginCredentials()

				# Attempts to login the user with their credentials provided
				results = self.model.attemptLogin(uid)

				if len(results) > 0:
					self.view.displayReport(uid, results)
				else:
					self.view.logMessage("No Report for this User: " + uid)

				# Moves to the main controller
				MainController.MainController(self.port).run(uid)

			elif authAction == 'Login as Anonymous':
				self.view.logMessage("Logged in anonymously")

				# Moves to the main controller
				MainController.MainController(self.port).run(-1)

			else: # Exit
				break

		return

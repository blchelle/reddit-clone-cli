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
		Runs through the authenticaiton process
		"""
		while (True):
			# Prompts and retrieves the users auth choice
			authAction = self.view.getAuthenticationAction()
			if(authAction == {} ):
				self.view.logMessage("#ERROR: Don't Click on the Options, Try again with keystrokes")
				continue
			authAction = authAction['auth method']

			if authAction == 'Login with Username':
				# Prompts and retrieves the users credentials
				credentials = self.view.getLoginCredentials()

				# Attempts to login the user with their credentials provided
				uid = credentials['uid']
				results = self.model.attemptLogin(uid)

				if results.count(True) > 0:
					self.view.displayReport(uid,results)
				else:
					self.view.logMessage("No Report for this User: "+uid)

				MainController.MainController(self.port).run(uid) # move to main controller

			elif authAction == 'Login as Anonymous':
				# Prompts and retrieves the desired uid
				uid = -1
				self.view.logMessage("Logged in as User: "+uid)

				MainController.MainController(self.port).run(uid) # move to main controller

			else: # Exit
				break
		return

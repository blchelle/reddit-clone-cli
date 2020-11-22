from models import authModel
from views import authView

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
				result = self.model.attemptLogin(credentials['uid'])

				# if result is not None:
				# 	MainController.MainController(self.port).run(credentials['uid']) # move to main controller
				# else:
				# 	self.view.logMessage("#ERROR: Wrong uid or password, Try again")


			elif authAction == 'Login as Anon':
				# Prompts and retrieves the desired uid
				print("ANON BOY")

			else: # Exit
				break
		return

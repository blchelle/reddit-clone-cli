"""
Phase 2 of the Reddit Clone CLI.
Main Controller

This file is responsible for ensuring clean communication between the
cli for the main menu (MainView) and the db (MainModel)

Contributors:
    Alireza Azimi
    Archit Siby
    Brock Chelle
"""
from views import view
from views import MainView
from models import MainModel
from controllers import PostsController

class MainController:
	def __init__(self, port):
		self.model = MainModel.MainModel(port)
		self.view = view.View()
		self.mainView = MainView.MainView()
		self.port = port
		self.postsController = PostsController.PostsController(port)


	def run(self, user):
		"""
		Runs through the main menu process

		Args:
			user: The uid of the user (-1 if anonymous)
		"""
		# Continuously prompt the user for the user until they specify "Log Out"
		while True:

			mainAction = self.mainView.getMainAction()
			if mainAction == {}:
				self.view.logMessage("#ERROR: Don't Click on the Options, Try again with keystrokes")
				continue

			mainAction = mainAction['action method']

			if mainAction == 'Post a question':
				# Prompts and recieves question values
				postValues = self.mainView.getQuestionPostValues()
				tagsList=postValues['tags'].strip().split()

				# Posts question to database
				self.model.postQuestion(postValues['title'], postValues['text'],tagsList,user)
				self.view.logMessage("Question posted successfully")
				continue

			elif mainAction == 'Search for questions':
				# Prompts and receives search values
				result = []
				postKeywords = self.mainView.getSearchValues()['keywords'].strip()

				if postKeywords == "":
					self.view.logMessage("#ERROR: Please enter one or more keywords to search for")
					continue
				else:
					s = postKeywords
					result = self.model.findQuestions(s)


				# Finds all search results from the database
				if result == []:
					self.view.logMessage("#NO MATCHING RESULTS, try a different keyword")
					continue
				self.view.logMessage("Results displayed below")

				# Counters for showing 5 results at a time
				pageSize = 10

				# Checks if the results needs pagination
				numPostsRemaining = len(result) - pageSize
				more = numPostsRemaining > 0

				# Displays the first page of results, and prompts for user input
				searchAction = self.mainView.getQuestionSearchAction(result[0:pageSize], more)
				if searchAction == {}:
					self.view.logMessage('#ERROR: Don\'t Click on the Options, Try again with keystrokes')
					continue

				searchAction = searchAction['action method']

				# Posting selected post to screen
				self.view.logMessage(" " + searchAction)

				# Show more results if the user specified to do so
				pageNumber = 0
				while searchAction == 'Show more results':
					pageNumber += 1

					# Checks if the results need pagination
					more = numPostsRemaining - pageSize > 0

					# Calculates where the page should start and stop
					startIndex = pageNumber * pageSize
					endIndex   = pageNumber * pageSize + min(numPostsRemaining, pageSize)

					# Displays the next page of results and prompts the user for a response
					searchAction = self.mainView.getQuestionSearchAction(
						result[startIndex : endIndex],
						more
					)

					# This is an edge case required for PyInquirer
					if searchAction == {}:
						self.view.logMessage('#ERROR: Don\'t Click on the Options, Try again with keystrokes')
						continue

					searchAction = searchAction['action method']
					numPostsRemaining -= pageSize

				# Navigates back to the main menu if the user specifies 'Back'
				if searchAction == "Back":
					continue

				# Retrieve the post id and go to post action menu
				selectedPost = searchAction.split()[0]
				PostsController.PostsController(self.port).run(user, selectedPost)

			else: # Log out
				return

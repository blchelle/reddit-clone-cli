"""
Phase 2 of the Reddit Clone CLI.
Posts Controller

This file is responsible for ensuring clean communication between the
cli for post actions (PostsView) and the db for posts (PostsModel)

Contributors:
    Alireza Azimi
    Archit Siby
    Brock Chelle
"""
from models import PostsModel
from models import authModel
from views import PostsView

class PostsController:
	def __init__(self, port):
		self.model = PostsModel.PostsModel(port)
		self.view = PostsView.PostsView()
		self.port = port


	def run(self, uid, pid):
		"""
		Runs through the post action process

		Args:
			uid: The uid of the authenticated user
			pid: The pid of the selected post
		"""
		# Updates the view to only show options available to the current user
		self.model.updateQuestionView(pid)

		# Gets information for the selected question, logs its information
		question = self.model.getPostsFromPid(pid)
		self.view.displayQuestion(question)

		postAction = ''
		while postAction != 'Back':

			# Prompts the user for the action they want to perform on the post
			postAction = self.view.getQuestionAction(uid == -1 or not self.model.userHasVotedOnPost(uid, pid))
			if postAction == {}:
				self.view.logMessage("#ERROR: Don't Click on the Options, Try again with keystrokes")
				continue

			postAction = postAction['questionAction']

			if postAction == "Answer Question":
				# Prompts the user for the body to an answer to the question
				postValues = self.view.getAnswerPostValues()
				body = postValues['body']

				# Writes the answer to the posts collection
				self.model.createAnswer(body, pid, uid)
				self.view.logMessage("Successfully added your answer")

			elif postAction == "List Answers":
				# Finds and displays all the answers to the question
				answersToQuestion = self.model.listAnswersForQuestion(pid)
				acceptedAnswerPid = self.model.getAcceptedAnswerId(pid)
				selectedAnswerPid = self.view.getAnswerListAction(answersToQuestion, acceptedAnswerPid)

				# Fetches the information for the selected answer, outputs it
				selectedAnswerInfo = self.model.getPostsFromPid(selectedAnswerPid)
				self.view.outputAnswerFields(selectedAnswerInfo)

				# Navigates to the answers menu
				self.runAnswers(uid, selectedAnswerPid)

			elif postAction == "Vote":
				# Adds a vote to the question in the db
				self.model.addVoteToPost(pid, uid)
				self.view.logMessage("Successfully upvoted post")
				continue

	def runAnswers(self, uid, aid):
		"""
		Runs the answers menu workflow

		Args:
			uid: The id of the authenticated user
			aid: The id of the answer post
		"""
		action = ''

		# Execute until the user selects back
		while action != 'Back':
			# Prompts the user for an action
			action = self.view.getAnswerAction(uid == -1 or not self.model.userHasVotedOnPost(uid, aid))

			# Votes on the post, if the user is authentcated, they can only do this once
			if action == "Vote":
				self.model.addVoteToPost(aid, uid)
				self.view.logMessage("Successfully upvoted post")

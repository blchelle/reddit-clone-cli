"""
Phase 2 of the Reddit Clone CLI.
Posts View

This file is responsible for interfacing with the user
for both the questions menu and the answers menu

Contributors:
	Alireza Azimi
	Archit Siby
	Brock Chelle
"""
from views import view
from PyInquirer import prompt

class PostsView(view.View):

	def getQuestionAction(self, userCanVote):
		"""
		Get action menu for questions

		Args:
			userCanVote: Determines if we should present a vote option for the user

		Returns:
			dict: The users action for the prompt
		"""
		# Builds the list of actions that the user can take
		actions = ["Answer Question", "List Answers"]
		if userCanVote:
			actions.append("Vote")
		actions.append("Back")

		questionActionPrompt = [
			{
				'type':'list',
				'message':'Select an action',
				'name':'questionAction',
				'choices': actions
			}
		]

		return prompt(questionActionPrompt, style=self.style)


	def getAnswerListAction(self, answers, acceptedAnswerPid):
		"""
		Display a list of answers and get input from the user to select one

		Args:
			answers: All the answers to display
			acceptedAnswerPid: The accepted answer pid

		Returns:
			str: The pid of the users selected answer
		"""
		actions=[]

		# Builds a list of all the results for list actions
		for answer in answers:
			id = answer['Id']

			body         = "".join(answer['Body'].split('\n'))
			creationDate = answer['CreationDate']
			score        = answer['Score']

			action = ''
			action += id + (7 - len(id)) * ' '

			if len(body) > 80:
				action += body[0:80] + "... "
			else:
				action += body[0:len(body)] + ((84 - len(body)) * " ")

			action += creationDate + ' '
			action += str(score)

			if acceptedAnswerPid == id:
				action += ' *'
				actions.insert(0, action)
			else:
				actions.append(action)

		questionActionPrompt = [
			{
				'type':'list',
				'message': ' Id' + 5 * ' ' + 'Body' + 80 * ' ' + 'Creation Date' + 11 * ' ' + 'Score',
				'name':'answerListAction',
				'choices': actions
			}
		]

		# This is required for PyInquirer, so that clicks don't cause a crash
		choice = {}
		while choice == {}:
			choice = prompt(questionActionPrompt, style=self.style)

			if choice == {}:
				self.logMessage('Error: Options cannot be selected by clicking on them')

		return choice['answerListAction'].split(' ')[0]


	def outputAnswerFields(self, answer):
		"""
		Logs all of the fields of an answer post to the console

		Args:
			answer: The answer document
		"""
		print('------------------ Selected Answer ------------------')
		for fieldName in answer:
			self.logMessage(fieldName + ': ' + str(answer[fieldName]))
		print('-----------------------------------------------------')


	def getAnswerAction(self, userCanVote):
		"""
		Displays a list of actions in the votes menu
		Prompts the user for an action

		Args:
			userCanVote: Determines if the user should have a vote option
		"""
		choices = []
		if userCanVote:
			choices.append('Vote')

		choices.append('Back')

		answerActionPrompt = [
			{
				'type':'list',
				'message': 'Select an action',
				'name':'answerAction',
				'choices': choices
			}
		]

		# This is required for PyInquirer, so that clicks don't cause a crash
		choice = {}
		while choice == {}:
			choice = prompt(answerActionPrompt, style=self.style)

			if choice == {}:
				self.logMessage('Error: Options cannot be selected by clicking on them')

		return choice['answerAction']


	def getAnswerPostValues(self):
		"""
		Prompts the user to enter title and body for an answer

		Returns:
			dict: The title and body of an answer
		"""
		postAnswerPrompts = [
			{
				'type': 'input',
				'message': 'Enter answer body: ',
				'name': 'body'
			}
		]

		return prompt(postAnswerPrompts, style=self.style)


	def displayQuestion(self, question):
		"""
		Outputs all the information for a question

		Args:
			question: The fields of a question document
		"""
		print("------------------ Selected Question ------------------")
		for fieldName in question:
			if fieldName in question:
				print(fieldName, question[fieldName])
		print("------------------------------------------------------")

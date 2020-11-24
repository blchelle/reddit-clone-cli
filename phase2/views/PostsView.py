from views import view
from PyInquirer import prompt


class PostsView(view.View):

    def getQuestionAction(self):
        """
        Get action menu for questions

        Returns
        -------
        Prompt message for question actions

        """
        actions = ["Answer Question", "List Answers", "Vote", "Back"]
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

        for fieldName in answer:
            self.logMessage(fieldName + ': ' + str(answer[fieldName]))

        print()


    def getAnswerAction(self):
        """
        """

        answerActionPrompt = [
            {
                'type':'list',
                'message': 'Select an action',
                'name':'answerAction',
                'choices': ['Vote', 'Back']
            }
        ]

        choice = {}
        while choice == {}:
            choice = prompt(answerActionPrompt, style=self.style)

            if choice == {}:
                self.logMessage('Error: Options cannot be selected by clicking on them')

        return choice['answerAction']


    def getAnswerPostValues(self):
        """
        Prompts the user to enter title and body for an answer

        Returns
        -------
        The title and body of an answer
        """

        postAnswerPrompts = [
            {
                'type': 'input',
                'message': 'Enter answer title:',
                'name': 'title'
            },
            {
                'type': 'input',
                'message': 'Enter answer body: ',
                'name': 'body'
            }
        ]

        return prompt(postAnswerPrompts, style=self.style)

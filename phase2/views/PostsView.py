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
                'type': 'list',
                        'message': 'Select an action',
                        'name': 'questionAction',
                        'choices': actions

            }
        ]

        return prompt(questionActionPrompt, style=self.style)

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

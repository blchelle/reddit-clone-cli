from views import view
from PyInquirer import prompt

class PostsView(view.View):

    def getQuestionAction(self):
        """


        Returns
        -------

        """
        actions=["Answer Question", "List Answers", "Vote", "Back"]
        questionActionPrompt = [
            {
                'type':'list',
				'message':'Select an action',
                'name':'questionAction',
                'choices': actions

            }
        ]

        return prompt(questionActionPrompt, style=self.style)

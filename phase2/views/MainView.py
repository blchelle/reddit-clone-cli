from views import view
from PyInquirer import style_from_dict, Token, prompt, Separator

class MainView(view.View):
    """
    A base class for views which is not intended to be instantiated
    """

    def getMainAction(self):
        """
        Asks the user what course of action they want to take

        Returns
        -------
        'Post a question' or 'Search for posts' or 'Exit'
        """

        options = [
            {
                'type': 'list',
                'message': 'Select an action',
                'name': 'action method',
                'choices': [
                    "Post a question",
                    "Search for questions",
                    "Log Out"
                ]
            }
        ]

        return prompt(options, style=self.style)

    def getQuestionPostValues(self):
        """
        Prompts the user to enter title and body for question

        Returns
        -------
        The title and body of question
        """

        postQuestionPrompts = [
            {
                'type': 'input',
                'message': 'Enter question title:',
                'name': 'title'
            },
            {
                'type': 'input',
                'message': 'Enter question body: ',
                'name': 'text'
            },
            {
                'type': 'input',
                'message': 'Enter zero or more tags: ',
                'name': 'tags'
            }
        ]

        return prompt(postQuestionPrompts, style=self.style)

    def getSearchValues(self):
        """
        Prompts the user to enter keyword to search for posts

        Returns
        -------
        keywords for searching
        """

        SearchPrompts = [
            {
                'type': 'input',
                'message': 'Enter one or more keyword to Search: ',
                'name': 'keywords'
            }
        ]

        return prompt(SearchPrompts, style=self.style)

    def findMaxLength(self, result):
        max_len = [0,0,0,0,0]
        for r in result:
            if len(r["Id"]) > max_len[0]:
                max_len[0] = len(r["Id"])
            if len(r["Title"]) > max_len[1]:
                max_len[1] = len(r["Title"])
            if len(r["CreationDate"]) > max_len[2]:
                max_len[2] = len(r["CreationDate"])
            if len(str(r["Score"])) > max_len[3]:
                max_len[3] = len(str(r["Score"]))
            if len(str(r["AnswerCount"])) > max_len[4]:
                max_len[4] = len(str(r["AnswerCount"]))
        return max_len

    def getQuestionSearchAction(self, results, showprompt):
        """
        Prompts the user to choose post from Search result

        Returns
        -------
        list of results that are selectable
        """

        header =  ' Id' + 5 * ' '
        header += 'Title' + 79 * ' '
        header += 'CreationDate' + 12 * ' '
        header += 'Score' + 2 * ' '
        header += 'AnswerCount'
 
        if(showprompt):
            results.append("Show more results")

        results.append("Back")


        postSearchPrompts = [
            {
                'type': 'list',
                'message': header,
                'name': 'action method',
                'choices': results
            }
        ]

        return prompt(postSearchPrompts, style=self.style)

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
                    "Search for posts",
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
            if len(r["CreationDate"].split("T")[0]) > max_len[2]:
                max_len[2] = len(r["CreationDate"].split("T")[0])
            if len(str(r["Score"])) > max_len[3]:
                max_len[3] = len(str(r["Score"]))
            if len(str(r["AnswerCount"])) > max_len[4]:
                max_len[4] = len(str(r["AnswerCount"]))
        return max_len

    def getQuestionSearchAction(self,results,max_len,showprompt):
        """
        Prompts the user to choose post from Search result

        Returns
        -------
        list of results that are selectable
        """
        max_len = self.findMaxLength(results)
        postList=[]
        header='Post Id'
        header+='  '+'Title'.ljust(23)
        header+='  '+'Creation Date'.ljust(max_len[2])
        header+='  '+'Score'.ljust(max_len[3])
        header+='  '+'Answer Count'.ljust(max_len[4])



        for post in results:
            pString = ""
            pString += post["Id"].ljust(max_len[0]) + "    "
            if len(post["Title"])>20:
                post["Title"] = post["Title"][0:20]+"..."
                max_len[1]=25
            pString += post["Title"].ljust(max_len[1]) + "  "
            pString += post["CreationDate"].split("T")[0].ljust(max_len[2]) + "     "
            pString += str(post["Score"]).ljust(max_len[3]) + "       "
            pString += str(post["AnswerCount"]).ljust(max_len[4]) + "  "
            postList.append(pString)

        if(showprompt):
            postList.append("Show more results")

        postList.append("Back")


        postSearchPrompts = [
            {
                'type': 'list',
                'message': header,
                'name': 'action method',
                'choices': postList
            }
        ]

        return prompt(postSearchPrompts, style=self.style)

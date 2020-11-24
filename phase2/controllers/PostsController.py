from models import PostsModel
from views import PostsView
from models import authModel

class PostsController:
    def __init__(self, port):
        self.model = PostsModel.PostsModel(port)
        self.view = PostsView.PostsView()
        self.port = port


    def run(self, uid, pid):
        """
        Runs through the post action process
        """
        self.model.updateQuestionView(pid)

        postAction = ''
        while postAction != 'Back':

            # Prompts the user for the action they want to perform on the post
            postAction = self.view.getQuestionAction()
            if(postAction == {} ):
                self.view.logMessage("#ERROR: Don't Click on the Options, Try again with keystrokes")
                continue
            postAction = postAction['questionAction']

            if postAction == "Answer Question":
                continue
            elif postAction == "List Answers":
                print('Question Id: ' + pid)
                answersToQuestion = self.model.listAnswersForQuestion(pid)
                selectedAnswerPid = self.view.getAnswerListAction(answersToQuestion)
                selectedAnswerInfo = self.model.getAnswerFromPid(selectedAnswerPid)
                self.view.outputAnswerFields(selectedAnswerInfo)
                self.runAnswers(uid, selectedAnswerPid)

            elif postAction == "Vote":
                continue

    def runAnswers(self, uid, pid):
        """
        Runs the answers menu
        """

        answerAction = ''
        while answerAction != 'Back':
            answerAction = self.view.getAnswerAction()

from models import model
import uuid
import sqlite3

class PostsModel(model.Model):
    dbname = '291db'
    def updateQuestionView(self, pid):
        """
		Updates view count for selected question

        """
        db = self.client[self.dbname]
        posts = db["Posts"]
        buffer = posts.find({"Id":pid})

        newCount = int(buffer[0]["ViewCount"]) + 1
        posts.update({"Id":pid},{"$set":{"ViewCount":str(newCount)}})

    def listAnswersForQuestion(self, pid):
        """
        Lists all the answers to a question with pid.

        Args:
            pid: The id field of the question post

        Returns:
            list(dict): All the answers for the question
        """

        # Gets the posts collection
        db = self.client[self.dbname]
        posts = db["Posts"]

        # Queries for all answer that answer the question
        results = []
        results.extend(posts.find(
            {
                '$and':
                    [
                        { "ParentId": pid },
                        { "PostTypeId": "2" }
                    ]
            },
            {
                "Id": 1,
                "Body": 1,
                "CreationDate": 1,
                "Score": 1
            }
        ))

        return results


    def getAnswerFromPid(self, pid):
        """
        Gets all the fields for a document from the posts collection
        This method should be called within the context of getting the info
        form an answer

        Args:
            pid: The pid of the answer post

        Return:
            dict: All the fields for the answer post
        """
        # Gets the posts collection
        db = self.client[self.dbname]
        posts = db["Posts"]

        # Queries for all answer that answer the question
        result = posts.find_one( { "Id": pid } )

        return result

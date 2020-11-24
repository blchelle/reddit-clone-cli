from models import model
from datetime import datetime
import uuid
import sqlite3

class MainModel(model.Model):

    def postQuestion(self, title, body, poster):
        """
        inserts question posts into the database


        Parameters
        ----------
        title : str
            title of question
        body : str
            body of question
        poster: str
            username of poster

        Return
        ----------
        None or {}

        """

        db = self.client["291db"]
        posts = db["Posts"]
        latestID=1
        latestIDs = posts.find().sort([("$natural",-1)]).limit(1)
        for doc in latestIDs:
            latestID = doc["Id"]
        
        newID = int(latestID)+1

        posts.insert({
            "Id":str(newID),
            "PostTypeId": "1",
            "CreationDate":datetime.now(),
            "Title": title,
            "Body": "<p>"+body+"</p>\n",
            "OwnerUserId": poster,
            "ContentLicense": "CC BY-SA 2.5"
            })
        


        # insertPostQuery = \
        # '''
        #     INSERT INTO posts
        #     VALUES (?,DATE('now', 'localtime'),?,?,?);
        # '''
        # insertQuestionQuery = \
        # '''
        #     INSERT INTO questions
        #     VALUES (?,?);
        # '''
        # try:
        #     # Executes and commits the query with the passed in parameters
        #     self.cursor.execute(insertPostQuery,(pid ,title, body, poster))
        #     self.cursor.execute(insertQuestionQuery, (pid, ""))
        #     self.connection.commit()
        # except sqlite3.Error as e:
        #     self.connection.rollback()
        #     print(e)
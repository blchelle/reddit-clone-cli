from models import model
from datetime import datetime
import uuid
import sqlite3
import re

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
        
        
    test="test"
    dbname = "291db"
    def findQuestions(self, searchString):
        """
		find questions based on keywords

        Returns
        -------
		list of matching questions

        """
        searchExpr = searchString.split(" ")
        patternList=[]
        results = []
        for keyWord in searchExpr:
            pattern = re.compile(".*" + keyWord + ".*", re.IGNORECASE)
            patternList.append(pattern)
        db = self.client[self.dbname]
        posts = db["Posts"]
        buffer = posts.find({"PostTypeId":"1", '$or':[
        {"Title":{'$in': patternList}},
        {"Body":{'$in': patternList}},
        {"Tags":{'$in': patternList}}]})
        results.extend(buffer)
        return results

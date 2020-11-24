from models import model
import uuid
import sqlite3
import re

class MainModel(model.Model):

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
            pattern = re.compile(".*" + keyWord + ".*")
            patternList.append(pattern)
        db = self.client[self.dbname]
        posts = db["Posts"]
        buffer = posts.find({"PostTypeId":"1", '$or':[
        {"Title":{'$in': patternList}},
        {"Body":{'$in': patternList}},
        {"Tags":{'$in': patternList}}]})
        results.extend(buffer)
        return results

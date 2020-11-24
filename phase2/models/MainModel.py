from models import model
import uuid
import sqlite3

class MainModel(model.Model):

    test="test"
    dbname = "291db"
    def findQuestions(self, searchString):
        # print(searchString)
        searchExpr = searchString.split(" ")
        results = []
        for keyWord in searchExpr:
            pattern = ".*" + keyWord + ".*"
            db = self.client[self.dbname]
            posts = db["Posts"]
            buffer = posts.find({"PostTypeId":"1", '$or':[
            {"Title":{'$regex': pattern,'$options':'i'}},
            {"Body":{"$regex": pattern, '$options':'i'}},
            {"Tags":{"$regex": pattern, '$options':'i'}}]})
            results.extend(buffer)
        return results

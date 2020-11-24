from models import model
import uuid
import sqlite3

class PostsModel(model.Model):
    dbname = '291db'
    def updateQuestionView(self, pid):
        db = self.client[self.dbname]
        posts = db["Posts"]
        buffer = posts.find({"Id":pid})

        newCount = int(buffer[0]["ViewCount"]) + 1
        posts.update({"Id":pid},{"$set":{"ViewCount":str(newCount)}})

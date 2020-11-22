from models import model
import sqlite3


class AuthModel(model.Model):

    def attemptLogin(self, uid):
        """
        Checks the users table to find a match of the username
        and password
        Parameters
        ----------
        uid : str
                The uid given at the command-line
        password : str
                The password given at the command-line
        Return
        ----------
        None or {}
                The result of the login query
                Return will be none if no such user is found
                Otherwise, the return will be the users information
        """

        # Template query for checking if the user is logged in

        db = self.client["291db"]
        posts = db["Posts"]
        results = posts.find({"OwnerUserId":uid})
        return results
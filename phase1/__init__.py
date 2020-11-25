"""
Phase 1 of the Reddit Clone CLI.

This application takes json files Posts.json, Tags.json, Votes.json and
converts then into MongoDB collections in a database running at some port number

Contributors:
    Alireza Azimi
    Archit Siby
    Brock Chelle
"""
import json
import sys
import re

from pymongo import MongoClient

relativePath = __file__.rpartition('/')[0]
if relativePath != '':
    relativePath += '/'

def printHelpMessage(message):
    """
    Print a help message for the user if they run the app with invalid arguments.

    Args:
        message: The first message to output to the user
    """
    print()
    print(message)
    print('This application expects a single argument <port-number>')
    print('Where 1023 < <port-number> < 65353\n')
    print('Example Command: `python3 __init__.py 8000`\n')
    sys.exit(-1)


def getPortNumber():
    """
    Check the command-line arguments for the port number.

    The program can exit in this method if
        Too few arguments are passed into the program
        Too many arguments are passed into the program
        The port number argument is non-numeric
        The port number argument is less than 0 since port numbers cannot be negative
        The port number argument is between 0 and 1023 since those ports are reserved
        The port number argument is larger than 65353 since that is the max port number

    Returns
        number: The port number passed into the program
    """
    if len(sys.argv) == 1:
        printHelpMessage('You passed too few command-line arguments into the application')
    elif len(sys.argv) > 2:
        printHelpMessage('You passed too many command-line arguments into the application')
    elif sys.argv[1].find('.') != -1:
        printHelpMessage('Port number `{}` is a decimal'.format(sys.argv[1]))

    try:
        portNumber = int(sys.argv[1])

        if portNumber < 0:
            printHelpMessage(
                'Port number `{}` is negative'.format(portNumber)
            )
        elif portNumber < 1024:
            printHelpMessage(
                'Port number `{}` is reserved for common TCP/IP applications'.format(portNumber)
            )
        elif portNumber > 65353:
            printHelpMessage(
                'Port number `{}` is higher than the maximum port number'.format(portNumber)
            )

        return portNumber

    except ValueError:
        printHelpMessage('You Passed a Non-Numeric Port Number Into the Application')


def initializeDb(portNumber):
    """
    Connect to the db server at the given port number.

    Attempts to connect to the db at the server
    If no db exists then it is created

    It checks the db for the collections 'Posts', 'Tags', 'Tags'
    If they exist then they are dropped and created
    They are created from json files in the same directory

    Args:
        portNumber: The port number where we will connect to the db
    """
    # Establishes a connection with the port
    client = MongoClient('localhost', portNumber)

    # Creates or opens the database on server.
    db = client['291db']

    # Gets the list of collections from the db
    collectionList = db.list_collection_names()
    print(collectionList)

    # Drops any of the collections if they exist
    for collection in collectionList:
        db[collection].drop()

    # Creates the 'Posts', 'Tags', 'Votes' collections
    insertJsonFileIntoDb('Posts.json', 'posts', db['Posts'])
    insertJsonFileIntoDb('Tags.json', 'tags', db['Tags'])
    insertJsonFileIntoDb('Votes.json', 'votes', db['Votes'])


def createPostsIndex(postsJson):
    """
    Insert a new field 'terms' which will be indexed for searching.

    Args:
        postsJson: The content of the Posts.json file

    Return:
        dict: The updated json which has the 'terms' entry for each post
    """
    for post in postsJson:
        bodyTerms = []
        titleTerms = []
        tagsTerms = []

        # Fetches the body and the title from the post
        body = post.get('Body')
        title = post.get('Title')
        tags = post.get('Tags')

        # Collects unique terms from the body, title, and tags
        if body is not None:
            bodyTerms = set(re.split('[^a-zA-Z0-9]', body.lower()))

        if title is not None:
            titleTerms = set(re.split('[^a-zA-Z0-9]', title.lower()))

        if tags is not None:
            tagsTerms = set("".join(tags.split('<')).split('>'))

        # Joins the set of terms
        terms = bodyTerms.union(titleTerms)
        terms = terms.union(tagsTerms)
        copyTerms = terms.copy()

        # Filters out all terms of length less than 3
        for term in copyTerms:
            if len(term) < 3:
                terms.remove(term)

        # Updates the post json
        post.update({'Terms': tuple(terms)})

    return postsJson


def insertJsonFileIntoDb(fileName, collectionName, collection):
    """
    Insert the content of a json file into a collection in the db.

    Args:
        filename: The name of the file, with the json extension
        collectionName: The name of the collection
        collection: The collection to inser into
    """
    # Read the JSON file
    print(relativePath +  fileName)
    with open(relativePath + fileName) as jsonFile:
        jsonContent = json.load(jsonFile)[collectionName]['row']

    if (collectionName is 'posts'):
        jsonContent = createPostsIndex(jsonContent)
        collection.create_index('Terms')

    # Inserts the data from the JSON file into the collection
    collection.insert_many(jsonContent)


if __name__ == "__main__":
    # Parses and Validates Command-Line Arguments for the Port Number
    portNumber = getPortNumber()

    # Connects and inserts collections into the data
    initializeDb(portNumber)

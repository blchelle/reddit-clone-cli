"""
Phase 1 of the Reddit Clone CLI.

This application takes json files Posts.json, Tags.json, Votes.json and
converts then into MongoDB collections in a database running at some port number

Contributors:
    Alireza Azimi
    Archit Siby
    Brock Chelle
"""
import sys


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


if __name__ == "__main__":
    portNumber = getPortNumber()

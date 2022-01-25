"""
This is the main file which installs dependencies if needed and then launches the program
"""

from subprocess import check_call
from sys import executable

def dep_check():
    """
    Checks dependencies and installs them if needed, then launches the main menu of the program.
    """
    try:
        __import__("colorama").__package__
    except ModuleNotFoundError:
        print("You do not have colorama, installing.")
        check_call([executable, "-m", "pip", "install", "colorama"])

    try:
        __import__("pyfiglet").__package__
    except ModuleNotFoundError:
        print("You do not have pyfiglet, installing.")
        check_call([executable, "-m", "pip", "install", "pyfiglet"])

    try:
        __import__("requests").__package__
    except ModuleNotFoundError:
        print("You do not have requests, installing.")
        check_call([executable, "-m", "pip", "install", "requests"])

    __import__("menu").MainMenu().menu()

if __name__ == "__main__":
    dep_check()

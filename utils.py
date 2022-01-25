"""
This file contains every utility function that is used in this program
"""

from random import choice
from string import digits, ascii_lowercase
from os import system, name
from sys import exit as clean_exit
from colorama import Style, Fore

PRIMARY = Fore.BLUE, Style.BRIGHT
SECONDARY = Fore.BLUE, Style.DIM

def random_string(length: int) -> str:
    """
    Returns a random string of selected length
    """
    final = []
    for _ in range(length):
        final.append(choice(digits + ascii_lowercase))
    return ''.join(final)

def clear_screen():
    """
    Clears the terminal
    """
    system('cls' if name == 'nt' else 'clear')

def get_option(chosen):
    """
    Gets the chosen option character from the option
    """
    return chosen[0].upper()

def get_colorful_text(attrs: tuple | list, text: str):
    """
    Returns the text with the Colorama attributes passed in
    """

    return(
        ''.join(attrs) +
        text +
        Style.RESET_ALL
    )

print_colorful_text = lambda attrs, text: print(get_colorful_text(attrs, text))

def surround_string(character: str, text: str):
    """
    This surrounds the supplied text with the supplied characters
    """

    total_len = 45
    text_len = len(text)
    surround_len = (total_len - text_len) / 2
    char_len = int(surround_len / len(character))
    return str(
        (character * char_len) +
        text +
        (character * char_len)
    )

def get_input(prompt: str, answer_type, options: list) -> str | int:
    """
    Retries an input statement until the user correctly types an answer,
    returns the answer in the correct type which has been passed in.
    """

    correct_answer = False
    answer = None
    while not correct_answer:
        print_colorful_text(PRIMARY, prompt)
        answer = input(''.join(SECONDARY))
        print(Style.RESET_ALL)
        if answer in [None, ""] or answer.isspace() \
            or options != [] and answer.upper() not in options:
            continue

        try:
            answer = answer_type(answer)
            correct_answer = True
        except(ValueError, TypeError):
            continue
        except KeyboardInterrupt:
            clean_exit()
    return str(answer)

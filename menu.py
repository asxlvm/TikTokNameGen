"""
This is a Python program to generate random strings and then automatically
check if a TikTok account with that string exists,
you can also use the From file option which will check
every string delimited by a space in a file.
"""

from threading import Thread
from time import sleep, time
from sys import exit as clean_exit
from colorama import Fore, Style, init
from colorama.ansi import set_title
from pyfiglet import Figlet
from requests import get
from requests.exceptions import ConnectionError as RequestsConnectionErr
from utils import surround_string, print_colorful_text, get_input, \
    get_option, clear_screen, random_string

init() # Enables ANSI escaping on Windows

SUCCESS = Fore.GREEN, Style.BRIGHT
ERROR = Fore.RED, Style.BRIGHT
WARNING = Fore.YELLOW
PRIMARY = Fore.BLUE, Style.BRIGHT
SECONDARY = Fore.BLUE, Style.DIM
FONT = Figlet(font="cosmic")
GENERATE = 0
FROM_FILE = 1

class GenerateMenu:
    """
    This is the generate menu class which handles generating the usernames,
    checking them and saving them
    """

    def __init__(self, gen_type: int):
        self.banner = str(
            FONT.renderText(
                "Gen\nMenu"
            ) +
            "\n" +
            surround_string("-", " Remade by @asxlvm ") +
            "\n"
        )
        self.options = ["[T]hreaded (faster)", "[N]on-threaded (slower)", "[B]ack\n"]
        self.checked = 1
        self.usernames_num = 0

        if gen_type == 0:
            self.str_type = "Generate"
            set_title("Name Gen by @asxlvm [Gen Menu - Generate]")
            self.menu(gen_type)

        elif gen_type == 1:
            self.str_type = "From file"
            set_title("Name Gen by @asxlvm [Gen Menu - From file]")
            self.menu(gen_type)

    def menu(self, gen_type):
        """
        This is the generate menu itself
        """
        self.available = []

        clear_screen()
        print_colorful_text(PRIMARY, self.banner)
        print_colorful_text(SECONDARY, f"Type: {self.str_type}")

        for option in self.options:
            print_colorful_text(SECONDARY, option)
        print_colorful_text(
            WARNING,
            "If you wanna force-close the program hit Control (Ctrl) + C and Enter\n"
        )
        is_threaded = get_input("What is your option?", str, ["T", "N", "B"])
        is_threaded = get_option(is_threaded)

        if is_threaded == "T":
            self.threaded = True

        elif is_threaded == "N":
            self.threaded = False

        elif is_threaded == "B":
            MainMenu().menu()

        if gen_type == 0:
            username_len = int(get_input(
                "How many letters should the username have?",
                int,
                []
            ))
            save_to = get_input(
                "What is the filename I should save the working usernames to?",
                str,
                []
            )
            generate_amt = int(get_input(
                "How many usernames should I generate and check?",
                int,
                []
            ))

            self.generate(
                username_len = username_len,
                generate_amt = generate_amt,
                save_to = save_to
            )

        elif gen_type == 1:
            filename = get_input(
                "What is the name of the file you wanna check?",
                str,
                []
            )
            save_to = get_input(
                "What is the filename I should save the working usernames to?",
                str,
                []
            )

            self.generate(
                filename = filename,
                save_to = save_to
            )

    def get_usernames(self, generate_amt = 0, username_len = 0, filename = None) -> list:
        """
        Generates / gets the usernames
        """

        usernames = []
        if self.str_type == "Generate":
            for _ in range(generate_amt):
                exists = True
                while exists:
                    username = random_string(username_len)
                    if username not in usernames:
                        exists = False
                        usernames.append(username)
        else:
            with open(filename, "r", encoding = "utf8") as file:
                usernames = file.read().split()
        return usernames

    def generate(self, generate_amt = 0, username_len = 0, filename = None, save_to = None):
        """
        Handles the checking and generating usernames
        """

        if self.str_type == "Generate":
            usernames = self.get_usernames(
                generate_amt = generate_amt,
                username_len = username_len,
            )
        else:
            usernames = self.get_usernames(
                filename = filename
            )

        self.usernames_num = len(usernames)
        clear_screen()

        start = time()

        if self.threaded:
            threads = []

            for username in usernames:
                threads.append(Thread(target=self.check, args=(username,)))

            for thread in threads:
                thread.start()
        else:
            for username in usernames:
                self.check(username)

        checked_all = False
        while not checked_all:
            if self.checked >= self.usernames_num:
                checked_all = True

        with open(save_to, "w", encoding = "utf8") as file:
            file.writelines(' '.join(self.available) + "\n")

        print_colorful_text(
            SUCCESS,
            f"\n{len(self.available)} available/banned out of {self.usernames_num}, " +
            f"checked {self.checked} usernames in {round(time() - start, 2)} seconds, " +
            f"saved into: {save_to} - going into main menu in 10 seconds"
        )
        sleep(10)
        MainMenu().menu()

    def check(self, username: str) -> bool:
        """
        Returns True if the said username is available / banned
        """

        set_title(f"Name Gen by @asxlvm [Generating: {self.checked}/{self.usernames_num}]")
        to_return = False
        url = "https://www.tiktok.com/@" + username
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;" +
                "q=0.9,image/webp,image/apng,/;" +
                "q=0.8,application/signed-exchange;v=b3;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Connection": "close",
            "Host": "www.tiktok.com",
            "Accept-Encoding": "gzip, deflate",
            "Cache-Control": "max-age=0"
        }

        try:
            response = get(url, headers = headers).status_code
        except RequestsConnectionErr as error_info:
            print_colorful_text(
                ERROR,
                f"{self.checked}/{self.usernames_num}: A connection error occured: {error_info}\n"
            )
            response = 0
        except KeyboardInterrupt:
            clean_exit()

        if response == 404:
            print_colorful_text(
                SUCCESS,
                f"{self.checked}/{self.usernames_num}: {username} - Available or Banned"
            )
            self.available.append(username)
            to_return = True

        if response == 0:
            pass

        else:
            print_colorful_text(
                ERROR,
                f"{self.checked}/{self.usernames_num}: {username} - Not Available"
            )

        self.checked += 1
        return to_return

class MainMenu:
    """
    This is the main menu class which then points you to another menu after choosing said menu
    """

    def __init__(self):
        self.banner = str(
            FONT.renderText(
                "Name\nGen"
            ) +
            "\n" +
            surround_string("-", " Remade by @asxlvm ") +
            "\n"
        )
        self.options = ["[G]enerate", "[F]rom file", "[C]redits", "[E]xit\n"]
        set_title("Name Gen by @asxlvm [Main Menu]")

    def menu(self):
        """
        This is the menu itself, this handles printing the banners, options
        and also redirects you to another menu
        """

        clear_screen()
        print_colorful_text(PRIMARY, self.banner)
        for option in self.options:
            print_colorful_text(SECONDARY, option)
        print_colorful_text(
            WARNING,
            "If you wanna force-close the program hit Control (Ctrl) + C and Enter\n"
        )

        option = get_input("What is your option?", str, ["G", "F", "C", "E"])
        option = get_option(option)
        if option == "G":
                GenerateMenu(GENERATE)

        elif option == "F":
                GenerateMenu(FROM_FILE)

        elif option == "C":
                self.credits()

        elif option == "E":
                clear_screen()
                clean_exit()

    def credits(self):
        """
        Prints the credits for this program
        """

        print_colorful_text(
            PRIMARY,
            "Original Creator: I don't even know, so many people skidded this, " +
            "the one I found is skidded by @2wbw\n"
        )
        print_colorful_text(
            PRIMARY,
            "Completely Remade by: @asxlvm on TikTok - Asylum#2206 on Discord - asxlvm on GitHub\n"
        )
        print_colorful_text(
            PRIMARY,
            "Link to Official Download: https://github.com/asxlvm/TikTokNameGen\n"
        )
        print_colorful_text(
            SECONDARY,
            "Press any key to go back."
        )
        input()
        self.menu()

"""
This file contains every utility function that is used in this program
"""

from random import choice
from string import digits, ascii_lowercase
from os import system, name
from sys import exit as clean_exit
from colorama import Style, Fore
from requests import post, get

PRIMARY = Fore.BLUE, Style.BRIGHT
SECONDARY = Fore.BLUE, Style.DIM
PROXIES = []

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

def scrapeproxies():
    global PROXIES

    scrapedproxies = get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=5000")
    for proxy in scrapedproxies.text.split("\n"):
        proxy = proxy.strip()
        if proxy:
            PROXIES.append(proxy)

def apicheck(username: str):
    """
    Checks if the username is banned or not, returns True or False
    """
    headers = {
        "accept-encoding": "gzip",
        "passport-sdk-version": "19",
        "sdk-version": "2",
        "x-tt-multi-SSIDs": "7025753269597127726%3Adfcf3163978d7473f4265b7985a97c8b%7C7026413601490617390%3A0baebad63036d3d61d7299db3e405ca5%7C7026441925374657583%3A3251cfad6fb8b282cceb4654e2e8d2af%7C7022383812068475909%3Ad087a612d20016e2176cefef2f999e70%7C7032340854528148527%3Ac1306e6dba4181c59f8621c41533cbf6%7C7033477327715976239%3A58aac7aae2ef19f2c936e58af2c74e0d%7C7033826104624284718%3Ac4b95aac0dfe8bb702314a057efcca4c%7C7033868646955631662%3Aa9507be4288abae1e7522b10c5a76413",
        "x-tt-token": "03a9507be4288abae1e7522b10c5a76413062e7ae4517c65574ddceac3cf8dc10f727e5057ba0d2f0832a31ddac9b9154891f5dd5d5cf2803cbfdc1db615db5d38bf8266ad9f8e509d112462c4b3b6d009a8b99ef707d2144c00b13f29274c9c8900b-1.0.1",
        "multi_login": "1",
        "x-tt-passport-csrf-token": "6753b5a64a0a0761bf0b8bbbb271405c",
        "x-ss-req-ticket": "1637702083512",
        "x-bd-client-key": "#p0SZ1fRy56diIMtyJvNIHp903FvyT7jENzv5Fm/TuAsNh5AsKEwE3pHP1LDFdnow0NeFTZq2IB4URkOm",
        "x-bd-kmsv": "0",
        "x-vc-bdturing-sdk-version": "2.2.1.i18n",
        "x-tt-dm-status": "login=1;ct=1;rt=1",
        "x-tt-cmpl-token": "AgQQAPNSF-RPsLGjvOP6vp0XxbkkhHRO_4fZYMPlzA",
        "x-tt-store-idc": "maliva",
        "x-tt-store-region": "us",
        "x-tt-store-region-src": "uid",
        "user-agent": "com.zhiliaoapp.musically/2022201040 (Linux; U; Android 7.1.2; en_US; A5010; Build/N2G48H;tt-ok/3.10.0.2)",
        "cookie": "sessionid=6753b5a64a0a0761bf0b8bbbb271405c",
        "x-ladon": "66i4D/A/9Duggct+t+TzgyNDPCpWofgabGLDBhqo5JcUg25R",
        "x-gorgon": "0404c0d24005a6dd2c0f90f095989f1cbbe822c080373f154aef",
        "x-khronos": "1637702083",
        "x-argus": "akF3zOzHe0jW4MD20rF9/IpQbtX2kWt7VmI17WF+n62ONJb7BvQO2kCiNlNutTEUeyxbpKFvQeKNZJfAODyxTM0vbS/9e9NWLaxmJNdsEr0ZOua7B2fZyxOetObzPkkkg1sL+DOi2Y5RsRTXNxhvRp3ndhSfmMHxN83rSR7/0pKIsabl/cLFXcV6r78ctYqOCLiSGFip0exaU1rP5re0ROKiSPauZGs7t2sJQXzyn8hfmKQywiGxdTZqKSZdecHYdmgbWBqHb99hzlqzusJdcRih73y+pRtse/j5IYpYa7hIjVjewRMbgwx7yHQ1hXXeibrjTW7m4XhzX38Gw0Ua8i99p2Fz9Y9WIzpCm591cBoOuQ==",
        "host": "api22-normal-c-useast1a.tiktokv.com",
        "connection": "Keep-Alive"
    }
    request = post("https://api22-normal-c-useast1a.tiktokv.com/passport/login_name/check/?passport-sdk-version=19&iid=7037880313762858758&device_id=6906478625937278469&ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=220105&version_name=22.1.5&device_platform=android&ab_version=22.1.5&ssmix=a&device_type=G011A&device_brand=google&language=en&os_api=25&os_version=7.1.2&openudid=c0575264c704f9c6&manifest_version_code=2022201050&resolution=1280*720&dpi=240&update_version_code=2022201050&_rticket=1638647824321&current_region=US&app_type=normal&sys_region=US&mcc_mnc=31610&timezone_name=AsiaShanghai&reSSIDence=US&ts=1638647824&timezone_offset=28800&build_number=22.1.5&region=US&uoo=0&app_language=en&carrier_region=US&locale=en&op_region=US&ac2=wifi&cdid=6ad560a8-8209-4fe3-b771-6bbe64880e4c&support_webview=1&okhttp_version=4.0.69.4-tiktok", headers=headers, params={"login_name": username}, proxies={"http": 'http://' + str(choice(PROXIES))})
    if "success" in request.text:
        return True
    return False

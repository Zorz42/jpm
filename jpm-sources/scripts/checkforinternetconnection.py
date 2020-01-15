import ssl
import urllib.error
import urllib.request

from globals import print_error, jpm_exit


def check_internet_connection():
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        urllib.request.urlopen("https://zorz.si")
        return True
    except urllib.error.HTTPError:
        return False


def check_connection():
    if not check_internet_connection():
        print_error("Cannot connect to the internet (zorz.si)")
        jpm_exit(1)

import ssl
import urllib.error
import urllib.request


def check_internet_connection():
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        urllib.request.urlopen("https://zorz.si")
        return True
    except urllib.error.HTTPError:
        return False

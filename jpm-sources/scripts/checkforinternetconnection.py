import urllib.request
import ssl


def check_internet_connection():
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        data = urllib.request.urlopen("https://google.com")
        return True
    except:
        return False

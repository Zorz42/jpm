import urllib.request


def check_internet_connection():
    try:
        data = urllib.request.urlopen("https://google.com")
        return True
    except:
        return False

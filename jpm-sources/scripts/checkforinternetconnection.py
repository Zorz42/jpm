import urllib.request

def check_internet_connection():
    try:
        data = urllib.request.urlopen("https://jaclang.zorz.si")
        return True
    except:
        return False

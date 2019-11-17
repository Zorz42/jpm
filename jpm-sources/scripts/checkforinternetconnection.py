import urllib

def check_internet_connection():
    try:
        stri = "https://jaclang.zorz.si"
        data = urllib.request.urlopen(stri)
        return True
    except:
        return False
        print("\x1b[0;31mCannot connect to jaclang.zorz.si")
        exit(1)

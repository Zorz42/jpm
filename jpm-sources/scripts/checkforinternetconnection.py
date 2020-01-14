import urllib.request
import ssl

from globals import *

def check_internet_connection():
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        data = urllib.request.urlopen("https://zorz.si")
        return True
    except:
        return False

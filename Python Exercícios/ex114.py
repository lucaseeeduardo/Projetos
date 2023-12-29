import urllib.request
try:
    page = urllib.request.urlopen("http://www.google.com.br").getcode()
    print("página acessível")
except:
    print('página inacessível')

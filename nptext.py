import requests
import base64
import json
from glob import glob
import pandas as pd
import time
import os
def ocr(IMAGE_PATH):
    import requests

    url = 'https://app.nanonets.com/api/v2/OCR/Model/b14cf25d-ca49-46e8-a1e8-a1911668036d/LabelFile/'

    data = {'file': open(IMAGE_PATH, 'rb')}

    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('ca49N499hj4hLD55CgqFOaNDUkHKuGaE', ''), files=data)

    k=response.text
    return k[186:197]

l=[]
c=0
for fn in glob('LP/*.jpg'):
    print("processing",c)
    c+=1
    l.append(ocr(fn))  
    if(c==3):
            break
l=set(l)
print(l)
for text in l:
    raw_data = {'date':[time.asctime( time.localtime(time.time()))],'':[text]}
    #raw_data = [time.asctime( time.localtime(time.time()))],[text]
    df = pd.DataFrame(raw_data)
    df.to_csv('data.csv',mode='a')
os.startfile('data.csv')     
        

import requests

url = 'https://app.nanonets.com/api/v2/OCR/Model/b14cf25d-ca49-46e8-a1e8-a1911668036d/LabelFile/'

data = {'file': open('frame1.jpg', 'rb')}

response = requests.post(url, auth=requests.auth.HTTPBasicAuth('ca49N499hj4hLD55CgqFOaNDUkHKuGaE', ''), files=data)

k=response.text
print(k[186:197])

import requests

url = 'https://app.nanonets.com/api/v2/OCR/Model/b14cf25d-ca49-46e8-a1e8-a1911668036d/LabelUrls/'

headers = {
    'accept': 'application/x-www-form-urlencoded'
}

data = {'urls' : ['https://goo.gl/ICoiHc']}

response = requests.request('POST', url, headers=headers, auth=requests.auth.HTTPBasicAuth('ca49N499hj4hLD55CgqFOaNDUkHKuGaE', ''), data=data)

print(response.text)

SECRET_KEY = 'sk_fa7d3dcec0363bdfb6ac3e06'
    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())
    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=ind&secret_key=%s' % (SECRET_KEY)  #Replace 'ind' with  your country code
    r = requests.post(url, data = img_base64)
    try:
        return(r.json()['results'][0]['plate'])
    except:
        print("No number plate found")

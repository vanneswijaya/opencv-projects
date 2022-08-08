import requests
import base64
import json

url = "https://api.riset.ai/api_tablet/v1/recognizemask"

image_filename = "/Users/vanneswijaya/Documents/PERSONAL/GALLERY/foto_selfie.jpg"

with open(image_filename, "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read())
    image_base64 = str(image_base64)[2:]
    image_base64 = str(image_base64)[:-1]
    f = open("response.txt", "a")
    f.write(str(image_base64))
    f.close()

    print("converted image to base64", image_base64)

print(type(image_base64))

payload = {"client_id" : "Trial",
            "trx_id" : "jfwoi902klf9sd7",
            "user_image" : str(image_base64),
            "timestamp" : "2020-01-01 00:00:00+07"}

# f = open("response.txt", "a")
# f.write(str(payload))
# f.close()
payload = str(payload)
# payload = json.loads(payload)

headers = {'content-type': 'application/json'}

response = requests.request("POST", url, data=payload, headers=headers)

data = json.loads(response.text)
print(data["return"])

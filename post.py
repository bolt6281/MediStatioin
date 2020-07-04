import json
import requests
import cv2
import time
import codecs

def post(uid, e_mail, url):

    data = {"id_medicine" : uid, "id_user": e_mail}
    headers = {'content-type': 'application/json'}
    res = requests.post(url ,data=json.dumps(data), headers=headers)
    print("json",res.json())

    return res.json()
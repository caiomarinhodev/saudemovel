# Send to single device.
from urllib2 import *
import urllib
import json
import sys


def func():
    MY_API_KEY = "AIzaSyBnlgWoujt6ti_spHWB12o2WZENKSaeDIY"

    messageTitle = "Pedido Novo Focus Delivery"
    messageBody = "Tem um novo pedido no aplicativo"

    data = {"to": "/topics/news",
            "notification": {"body": messageBody, "title": messageTitle, "icon": "ic_cloud_white_48dp", "sound": "default"}}

    dataAsJSON = json.dumps(data)

    request = Request("https://gcm-http.googleapis.com/gcm/send", dataAsJSON,
                      {"Authorization": "key=" + MY_API_KEY, "Content-type": "application/json"})
    resp = urlopen(request).read()
    print(resp)
    return resp

import io
import pycurl
from urllib.parse import urlencode
import certifi
import json
from io import StringIO
from io import BytesIO


# curl --header "Authorization: key=AAAAU-t18ok:APA91bFXOcTsKYn2H53SrT6fO-nDae8YKQhE7_FqSp7odzjYZrm7je8jN_f8Sea9TwovismPGyAvNhGozhd1ZlyrGQ2NYpQFxO4g_pn5cDa1_xX2JycpcsPH1AJ_Bad5KcjDpeyjQ6wn" --header Content-Type:"application/json" https://fcm.googleapis.com/fcm/send -d "{\"to\":\"/topics/weather13_fcm_one\", \"priority\":\"high\", \"data\": {\"notificationTitle\":\"\",\"flag\":\"n\",\"notificationMessage\":\"8 16 20\",\"notificationContent\":\"VuNIsY6JdUw\",\"notificationUrl\":\"\"}}"

def postCurl():
    c = pycurl.Curl()
    # stringio = io.StringIO
    url = 'https://fcm.googleapis.com/fcm/send'
    header1 = [
        'Authorization: key=AAAAU-t18ok:APA91bFXOcTsKYn2H53SrT6fO-nDae8YKQhE7_FqSp7odzjYZrm7je8jN_f8Sea9TwovismPGyAvNhGozhd1ZlyrGQ2NYpQFxO4g_pn5cDa1_xX2JycpcsPH1AJ_Bad5KcjDpeyjQ6wn'
        , 'Content-Type: application/json']

    postdate = {
        "to": "/topics/weather13_fcm_one",
        "priority": "high",
        "data": {
            "notificationTitle": "",
            "flag": "n",
            "notificationMessage": "8 16 20",
            "notificationContent": "VuNIsY6JdUw",
            "notificationUrl": ""
        }
    }

    byteio = io.BytesIO()

    c.setopt(pycurl.CAINFO, certifi.where())
    c.setopt(pycurl.URL, url)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.VERBOSE, True)

    c.setopt(pycurl.HTTPHEADER, header1)
    c.setopt(pycurl.POSTFIELDS, json.dumps(postdate))
    c.setopt(pycurl.WRITEDATA, byteio)
    c.setopt(pycurl.PROXY, '127.0.0.1')
    c.setopt(pycurl.PROXYPORT, 1080)
    c.perform()
    c.close()

    body = byteio.getvalue().decode('utf-8')
    print(body)


postCurl()

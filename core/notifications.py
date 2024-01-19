from django.contrib.auth.models import User
from webpush import send_user_notification
import json
from urllib.request import urlopen


def send_notification(data):
    user_id = data['user']
    user = User.objects.get(id=user_id)
    head = data['head']
    body = data['body']
    icon = ''
    payload = {'head': head, 'body': body, 'url': "https://www.example.com"}
    send_user_notification(user=user, payload=payload, ttl=1000)


def sms_notification(data):
    sms_api_key = 'ed0n7qieVmnsYHlyXZAQnNBTkkeu1Z24pW4npKZi'
    sms_msg_str = data['message']
    sms_msg = sms_msg_str.replace(" ", "%20")  # replacing spaces with %20
    sms_to = data['phone_no']
    # url = "https://api.sms.net.bd/sendsms?api_key="+sms_api_key+"&msg="+sms_msg+"&to="+sms_to
    url = "https://www.google.com"
    # response = urlopen(url)
    # data_json = json.loads(response.read())
    return print(url)

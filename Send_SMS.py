import os
from twilio.rest import Client

def sendsms(number,msgtype,body):
    switcher = {1:'Confirmation',
                2:'Status',
                3:'Reminder'
               }
    body = switcher.get(msgtype) + ':  ' + body
    
    client = Client('ACa9d6a5db71635a21886b2777008758c0', '536fccfba9512a7729cfaa553d5e11a2')

    message = client.messages \
                    .create(
                         body=body,
                         from_='HSPTLEYES',
                         to=number
                     )

    print(message.sid)

    numlist = ['+4915258473908','+4915165754071','+491722448758','+491788234066','+4915737828196']



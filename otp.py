
from twilio.rest import Client
import requests

# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
TWILIO_SID='' # Id using alsafenoreply@gmail.com
TWILIO_AUTHTOKEN=''

TWILIO_MESSAGE_ENDPOINT = 'https://api.twilio.com/2010-04-01/Accounts/{id}/Messages.json'
TWILIO_NUMBER = 'whatsapp:+number'
def send_whatsapp_message(to, message):
    message_data = {
        "To": to,
        "From": TWILIO_NUMBER,
        "Body": message,
    }
    response = requests.post(TWILIO_MESSAGE_ENDPOINT, data=message_data, auth=(TWILIO_SID, TWILIO_AUTHTOKEN))

    response_json = response.json()


    return response_json

# client = Client(TWILIO_SID,TWILIO_AUTHTOKEN)
#
# message = client.messages.create(
#                               body='Hello there!',
#                               from_='whatsapp:+14155238886',
#                               to='whatsapp:+919440775280'
#                           )
#
# print(message.sid)
# print(message)

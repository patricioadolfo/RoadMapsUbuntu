# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid.sendgrid import SendGridAPIClient 

from sendgrid.helpers.mail import Mail

def send_mail():

    message = Mail(
        from_email='violetalamonicaprimaria@gmail.com',
        to_emails='patricioadolfo@outlook.es',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(api_key='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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


send_mail()
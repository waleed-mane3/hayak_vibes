import smtplib
from email.message import EmailMessage
from django.conf import settings


# Request Email
def send_confirmation_email(sender_name, recipient_name, recipient_email, reference_id):
    # sender_server = 'Info@aiartathon.com'
    sender_email = 'kareemahmad19995@gmail.com'
    password_email = '@$^*Kareem_1995'

    msg = EmailMessage()
    msg['Subject'] = f'Wedding invitation from {sender_name}'
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Reply-To'] = sender_email

    msg.add_alternative(f'''\
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body>
                <p>Hi <strong>{recipient_name}</strong></p>
                <p>I am pleased to invite you to witness my moment</p><br /> <br />
                <p>please confirm your attendence</p>
                <a href="{settings.BASE_URL}/api/account/accept_invitation/{reference_id}/">I confirm</a>
                <a href="{settings.BASE_URL}/api/account/reject_invitation/{reference_id}/">I, apologize</a>
            </body>
        </html>
    ''', subtype='html')

    # Start The connection with Mail Server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password_email)
    server.send_message(msg)
# End Email


import smtplib
#allows us to send text and emails
from email.mime.text import MIMEText
from config import Config


#mailtrap.io

def send_mail(customer,dealer, rating, comments):
    port = Config['port']
    smtp_server = Config['smtp_server']
    login = Config['login']
    password = Config['password']
    message = f"<h3> new feedback submission</h3><ul><li>{customer}</li><li>{dealer}</li><li>{rating}</li><li>{comments}</li></ul>"
    sender_email = Config['sender_email']
    receiver_email = Config['receiver_email']
    msg = MIMEText(message, 'html')
    msg['Subject'] = "feedback"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    #sending email

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


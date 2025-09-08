import smtplib

sender = 'shrijwalabus@gmail.com'
app_password = 'anpigtlqytdjetnz'  # No spaces!
receiver = 'swapnilmishrak2230@gmail.com'
subject = 'Test Email'
body = 'This is a test email from Shrijwala app.'

email_text = f"""\
From: {sender}
To: {receiver}
Subject: {subject}

{body}
"""

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, app_password)
        server.sendmail(sender, receiver, email_text)
    print('Test email sent successfully!')
except Exception as e:
    print('Error sending test email:', e) 
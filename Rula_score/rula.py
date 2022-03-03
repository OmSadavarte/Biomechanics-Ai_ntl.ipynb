import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
sender_email = "omprasadsadavarte@gmail.com"
receiver_email = "om9420@srmist.edu.in"
password = input("Type your password and press enter:")
message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email
text = """\
Hi,
"""
html = """\
<html>

<head>
	<title>Regarding Posture Correction- Biomechanics-Ai Ltd.</title>
</head>

<body>
	This is to notify that your posture seems incorrect and Reba scores seem concerning, 
	please sit upright and consult a phsiologist.

	sincere Regards
	Biomechanics Ltd.
</body>

</html>

"""
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
message.attach(part1)
message.attach(part2)
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import sys

def send_email(photos, to_email, smtp_server, smtp_port, smtp_user, smtp_password):

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")

    subject = f"Intruder {current_date} // {current_time}"
    body = f"An intruder or incident has been detected on the detector on {current_date} at {current_time}. Images captured by the camera will be attached."

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for photo in photos:
        with open(photo, 'rb') as file:
            img = MIMEImage(file.read())
            img.add_header('Content-Disposition', f'attachment; filename={os.path.basename(photo)}')
            msg.attach(img)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())
            print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    photos = sys.argv[1:]  

    from_email = "poolswagstyle@gmail.com" 
    to_email = "pablo.jimenez-torr@yorksj.ac.uk"  
    smtp_server = "smtp.gmail.com"  
    smtp_port = 587  
    smtp_user = from_email  
    smtp_password = "fnncxokoebycgnch"  

    send_email(photos, to_email, smtp_server, smtp_port, smtp_user, smtp_password)

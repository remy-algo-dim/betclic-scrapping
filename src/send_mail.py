import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os

load_dotenv()

MAIL = os.getenv('MAIL')
PSWD = os.getenv('PSWD')


def send_notifications(emailfrom, emailto, body, attachment_path=None):
    # Créer l'objet MIMEMultipart pour l'e-mail
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ", ".join(emailto)
    msg["Subject"] = "Betclic scrap"

    # Ajouter le texte de l'e-mail
    msg.attach(MIMEText(body, "plain"))

    # Ajouter la pièce jointe CSV
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachment_path.split('/')[-1]}"
    )
    msg.attach(part)

    # Envoyer l'e-mail
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    server.ehlo()
    server.starttls()
    server.login(MAIL, PSWD)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()

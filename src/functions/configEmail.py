import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from dotenv import load_dotenv
import os
load_dotenv()

# definindo a função send_email
def send_email(to, subject, body, name):
    # configurando a mensagem do e-mail
    msg = MIMEMultipart()
    msg['From'] = os.environ.get('EMAIL')
    msg['To'] = to
    msg['Subject'] = subject

    # adicionando o corpo do e-mail
    body_text = f"Olá {name}, segue seu código para verificar o email:\n\n{body}"
    msg.attach(MIMEText(body_text, 'plain'))

    # criando a conexão SMTP e envie o e-mail
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(os.environ.get('EMAIL'), os.environ.get('PASSWORD'))
    s.sendmail(os.environ.get('EMAIL'), to, msg.as_string())
    s.quit()
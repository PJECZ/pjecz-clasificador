import imaplib
import smtplib
import email
import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import time

#logs in to the desired account and navigates to the inbox
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('informaticapjecz@gmail.com','PoderJudicial*')
mail.list()

while True:
    mail.select('inbox') #acceso a la carpeta principal con permisos de lectura
    type, data = mail.search(None, 'UNSEEN') # busca los correos que no han sido leido
    mail_ids = data[0]
    id_list = mail_ids.split()
    
    #recorre los correos por id
    for num in data[0].split():
        latest_email_uid = id_list[-1]
        typ, data = mail.fetch(num, '(RFC822)' )
        raw_email = data[0][1]
        latest_email_uid = id_list[-1]
        # converts byte literal to string removing b''
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        # downloading attachments
        for part in email_message.walk():
            fileName = part.get_filename()
            #valida que  el correo tenga un archivo adjunto si no encuentra archivo adjunto no descarga y continual la busqueda cada determinado tiempo
            if bool(fileName):
                filePath = os.path.join('C:/hello/', fileName) #se especifica la ruta donde se almacena el archivo descargado
                if not os.path.isfile(filePath) :
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

                emailnot = ''
                if email_message.is_multipart():
                    emailnot =  email_message['From']
                    #muestro datos en terminal del correo electronico que se trabajo
                    print('Downloaded "{file}"'.format(file=fileName))
                    print('To:\t\t', email_message['To'])
                    print('From:\t', email_message['From'])
                    print('Subject:', email_message['Subject'])
                    print('Date:\t',email_message['Date'])
                
                ###  #Enviar correo de respuesta
               
                username = 'informaticapjecz@gmail.com'  # Email Address from the email you want to send an email
                password = 'PoderJudicial*' # Password
                server = smtplib.SMTP('smtp.gmail.com:587')

                """
                SMTP Server Information
                1. Gmail.com: smtp.gmail.com:587
                2. Outlook.com: smtp-mail.outlook.com:587
                3. Office 365: outlook.office365.com
                Please verify your SMTP settings info.
                """

                # Create the body of the message (a HTML version for formatting).
                html = """Constancia de recibo - Edictos"""

                # Function that send email.
                def send_mail(username, password, from_addr, to_addrs, msg):
                    server = smtplib.SMTP('smtp.gmail.com', '587')
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(username, password)
                    server.sendmail(from_addr, to_addrs, msg.as_string())
                    server.quit()

                # email
                from_addr = 'informaticapjecz@gmail.com'
                to_addrs = emailnot

                msg = MIMEMultipart()

                msg['Subject'] = "Constancia de recibo - Edictos"
                msg['From'] = from_addr
                msg['To'] = to_addrs

                # Attach HTML to the email
                body = MIMEText(html, 'html')
                msg.attach(body)

                # Attach Cover Letter to the email
                cover_letter = MIMEApplication(open("acuse_de_recibo_edictos.pdf", "rb").read())
                cover_letter.add_header('Content-Disposition', 'attachment', filename="acuse_de_recibo_edictos.pdf")
                msg.attach(cover_letter)

                try:
                    send_mail(username, password, from_addr, to_addrs, msg)
                    print("Email successfully sent")
                except:
                    print('SMTPAuthenticationError')
                    print('Email not sent to')

    time.sleep(15) #cada 10 segundo lee un correo electronico en estatus de "no leido"




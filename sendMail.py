from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import getpass
import configparser
import os
import smtplib
 
# load config file
cfg = configparser.ConfigParser()
cfg.read('conf.ini')
# list files to attachment
directory  = os.listdir(cfg.get('general', 'path'))
files = [arq for arq in directory if arq.lower().endswith(cfg.get('general', 'type'))]
# get mail password
password = getpass.getpass("Password: ")

# send a mail to each attachment
for fileName in files:
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message    
    msg['From'] = cfg.get('server', 'from')
    msg['To'] = cfg.get('server', 'to')
    msg['Subject'] = "Arquivo: %s" % fileName
    
    # add in the message body
    message = "Arquivo: %s" % fileName
    msg.attach(MIMEText(message, 'plain'))

    # add in the message attachment
    attachment = open(cfg.get('general', 'path') + '\\' + fileName, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % fileName)
    msg.attach(part)
    
    #create server
    server = smtplib.SMTP(cfg.get('server', 'smtp') + ': ' + cfg.get('server', 'port'))
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password) 
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    
    print("%s successfully sent to %s" % (fileName, msg['To']))
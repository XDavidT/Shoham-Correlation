import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from CacheHandler import *
from ActionsHandlers.EmailContentGen import HTML_Template


def AlertOnEmail(log_document):
    alrt_set = load_alert_setting()
    msg_content = GetMsgContent(alrt_set)

    msg_content['Subject'] = 'Important event from SIEM system'
    msg_content.attach(MIMEText(HTML_Template(log_document), 'html'))  # Using Html Generator in package

    server = GetServer(alrt_set)
    server.sendmail(alrt_set['email-username'], 'xdavidt@gmail.com', msg_content.as_string())
    server.quit()
    print("Email sent!")


def GetServer(alrt_set):
    serv = smtplib.SMTP(alrt_set['smtp-server'], alrt_set['smtp-server-port'])
    serv.starttls()
    serv.login(alrt_set['email-username'], alrt_set['email-password'])
    return serv

def GetMsgContent(alrt_set):
    msg_content = MIMEMultipart('alternative')
    msg_content['From'] = alrt_set['email-username']
    msg_content['To'] = 'xdavidt@gmail.com'
    return msg_content
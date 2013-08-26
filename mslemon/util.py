import smtplib
from email.MIMEText import MIMEText

from mslemon.models.usergroup import User

def make_email_message(subject, message, sender, receiver):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    return msg

def send_email_through_smtp_server(settings, message, sender, receiver):
    prefix = 'mslemon.smtp.'
    server = settings[prefix + 'server']
    port = int(settings[prefix + 'port'])
    login = settings[prefix + 'login']
    password = settings[prefix + 'password']
    server = smtplib.SMTP(server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login, password)
    msg = message.as_string()
    server.sendmail(sender, receiver, msg)
    server.close()


import os
from datetime import datetime, timedelta

testname = '130501151028_0001.pdf'

def datetime_from_pdf_filename(filename):
    dtstring = filename.split('_')[0]
    year = int(dtstring[0:2]) + 2000
    month = int(dtstring[2:4])
    day = int(dtstring[4:6])
    hour = int(dtstring[6:8])
    minutes = int(dtstring[8:10])
    seconds = int(dtstring[10:12])
    return datetime(year, month, day, hour, minutes, seconds)

def get_scanned_filenames(directory):
    filenames = os.listdir(directory)
    now = datetime.now()
    prefix = str(now.year - 2000)
    filenames = (f for f in filenames if f.startswith(prefix))
    filenames = (f for f in filenames if len(f) == 21)
    filenames = (f for f in filenames if f.index('_') == 12)
    return filenames


def get_scanned_pdfs(directory):
    filenames = get_scanned_filenames(directory)
    dts = [datetime_from_pdf_filename(f) for f in filenames]
    #return dict(zip(filenames, dts))
    content = ''
    for f in filenames:
        fp = os.path.join(directory, f)
        content += file(fp).read()
    return len(content)/ 1024.0 / 1024.0

def get_scanned_pdfs_request(request):
    settings = request.registry.settings
    dirname = settings['mslemon.scans.directory']
    return get_scanned_pdfs(dirname)


def get_regular_users(request):
    users = request.db.query(User).all()
    skey = 'mslemon.admin.admin_username'
    admin_username = request.registry.settings.get(skey, 'admin')
    return [u for u in users if u.username != admin_username]




if __name__ == "__main__":
    pass

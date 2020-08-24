import smtplib
import gnupg
import os
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

servers = ['disroot.org', 'gmail.com', 'posteo.net', 'yahoo.com', 'live.com']
cockliservers = ['cock.li','airmail.cc','420blaze.it','aaathats3as.com','cumallover.me','goat.si','horsefucker.org','national.shitposting','nigge.rs','tfwno.gf','cock.lu','cock.email','firemail.cc','hitler.rocks','getbackinthe.kitchen','memeware.net','cocaine.ninja','waifu.club','rape.lol','nuke.africa']

userpath = os.getcwd()
user = getpass.getuser()
encryptedpassword = open('password.txt.asc').read()
encryptedusername = open('email.txt.asc').read()
gpg = gnupg.GPG(gnupghome=f'/home/{user}/.gnupg')
SenderFingerprint = str(input('Enter email associated with your public key or key fingerprint (doesn\'t have to be your sending email address): '))
SenderID = SenderFingerprint.replace(' ','')
pkey = gpg.export_keys(SenderID)
pubkey = open('publickey.txt', 'w')
pubkey.write(pkey)
pubkey.close()
decryptedpassword = str(gpg.decrypt(encryptedpassword))
password = decryptedpassword.partition('\n')[0]
decryptedusername = str(gpg.decrypt(encryptedusername))
username = decryptedusername.partition('\n')[0]
providername = username.split('@',1)[1]
TLS_port = 587

if any(providername in i for i in servers):
    if providername == 'disroot.org':
        server = providername
    elif providername == 'gmail.com':
        server = 'smtp.gmail.com'
        print('You need to add app password from your Google account for this script to work, in case of error visit: \nhttps://support.google.com/accounts/answer/185833?hl=en')
    elif providername == posteo.net:
        server = 'posteo.de'
    elif providername == 'startmail.com':
        server = 'smtp.startmail.com'
    elif providername == 'yahoo.com':
        server = 'smtp.mail.yahoo.com'
    elif providername == 'live.com':
        server = 'smtp.live.com'
    else:
        print('Provider not in the list of providers, contact maintainer of this project for adding provider you use to list.')

if any(providername in i for i in cockliservers):
    server = 'mail.cock.li'
query = str(input('Attach your public key? (yes|no): ')).lower()

msg = MIMEMultipart()

def attachment():
    publickey = 'publickey.txt'
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(open(userpath + '/publickey.txt', 'rb').read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % publickey)
    msg.attach(p)

def email():
    msg['From'] = username
    RecipientFingerprint = str(input('Recipient fingerprint or email address associated with that fingerprint: '))
    RecipientID = RecipientFingerprint.replace(' ','')
    Recipient = str(input('Recipient email: '))
    msg['To'] = Recipient
    msg['Subject'] = 'PGP message'
    mailbody = str(input('Enter your secret message: '))
    secretmessage = (str(gpg.encrypt(mailbody, RecipientID )))
    msg.attach(MIMEText(secretmessage, 'plain'))
    return Recipient

def authentication(Recipient):
    smtpObj = smtplib.SMTP(server, TLS_port)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.ehlo()
    smtpObj.login(username, password)
    try:
        smtpObj.sendmail(username, Recipient, msg.as_string())
        smtpObj.close()
        print('\nMessage successfully sent!')
    except Exception as e:
        print(e)

if query == 'yes':
    Recipient = email()
    attachment()
    authentication(Recipient)
    
elif query == 'no':
    Recipient = email()
    authentication(Recipient)
else:
    print('Please type in yes or no.')
os.remove(userpath + '/publickey.txt')

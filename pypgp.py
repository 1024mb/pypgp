import smtplib
import gnupg
import os
import getpass
import platform
import sys
import argparse

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def attachment(userpath, msg):
    publickey = "publickey.txt"
    p = MIMEBase("application", "octet-stream")
    p.set_payload(open(userpath + "/publickey.txt", "rb").read())
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", "attachment; filename= %s" % publickey)
    msg.attach(p)

def email(msg, username, gpg, RecipientFingerprint, RecipientEmail, EmailSubject, EmailMessage):
    # print("\nmsg, username, gpg, RecipientFingerprint, RecipientEmail, EmailSubject, EmailMessage \n")
    # print(msg, "\n", username, "\n", gpg, "\n", RecipientFingerprint, "\n", RecipientEmail, "\n", EmailSubject, "\n\N", EmailMessage, "\n")
    msg["From"] = username
    if RecipientFingerprint is None:
        RecipientFingerprint = str(input("Recipient fingerprint or email address associated with that fingerprint: "))
        if RecipientFingerprint == "":
            print("ERROR: You have to enter a recipient fingeprint, exiting...")
            sys.exit(1)
    RecipientID = RecipientFingerprint.replace(" ","")
    if RecipientEmail is None:
        RecipientEmail = str(input("Recipient email: "))
        if RecipientEmail == "":
            print("ERROR: You have to enter a recipient email, exiting...")
            sys.exit(1)
    msg["To"] = RecipientEmail
    msg["Subject"] = EmailSubject
    if EmailMessage is None:
        EmailMessage = str(input("Enter your private message: "))
        if EmailMessage == "":
            print("ERROR: You have to enter a message, exiting...")
            sys.exit(1)
    privatemessage = (str(gpg.encrypt(EmailMessage, RecipientID )))
    msg.attach(MIMEText(privatemessage, "plain"))
    return RecipientEmail

def authentication(Recipient, server, TLS_port, username, password, msg):
    # print("\n\nRecipient, server, TLS_port, username, password, msg\n")
    # print(Recipient, "\n", server, "\n", TLS_port, "\n", username, "\n", password, "\n", msg, "\n\n")
    smtpObj = smtplib.SMTP(server, TLS_port)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.ehlo()
    smtpObj.login(username, password)
    try:
        smtpObj.sendmail(username, Recipient, msg.as_string())
        smtpObj.close()
        print("\nMessage successfully sent!")
    except Exception as e:
        print(e)
        print(Recipient, "\n", server, "\n", TLS_port, "\n", msg )
        sys.exit(1)

def main():

    parser = argparse.ArgumentParser(
        description="Send PGP encrypted email"
    )
    parser.add_argument("--ae", "--associated-email", help="Associated email with public key or key fingerprint", metavar="ASSOCIATED-EMAIL")
    parser.add_argument("--rf", "--recipient-fingerprint", help="Recipient fingerprint", metavar="RECIPIENT-FINGERPRINT")
    parser.add_argument("--re", "--recipient-email", help="Recipient email", metavar="RECIPIENT-EMAIL")
    parser.add_argument("--m", "--message", help="The private message you want to send", metavar="MESSAGE")
    parser.add_argument("--pf", "--password-file", help="Specify password file, default is password.txt.asc (Optional)", metavar="%PASSWORD-FILE%", default="password.txt.asc")
    parser.add_argument("--ef", "--email-file", help="Specify email file, default is email.txt.asc (Optional)", metavar="%EMAIL-FILE%", default="email.txt.asc")
    parser.add_argument("--pt", "--port", help="Specify a TLS port (Optional)", metavar="PORT", type=int, default=587)
    parser.add_argument("--at", "--attach", help="Attach public key to email (Optional)", action="store_true")
    parser.add_argument("--s", "--subject", help="Specify the subject for the email (Optional)", default="PGP Message", metavar="SUBJECT")
    parser.add_argument("--ms", "--manual-server", help="Specify server manually (Optional)", metavar="smtp.example.com")
    parser.add_argument("--pp", "--passphrase", help="Specify the passphrase to use (Optional)", metavar="PASSPHRASE")
    args = parser.parse_args()

    cockliservers = ["cock.li","airmail.cc","420blaze.it","aaathats3as.com","cumallover.me","goat.si","horsefucker.org","national.shitposting.agency","tfwno.gf","cock.lu","cock.email","firemail.cc","memeware.net","cocaine.ninja","waifu.club","dicksinhisan.us","loves.dicksinhisan.us","wants.dicksinhisan.us","dicksinmyan.us","loves.dicksinmyan.us","wants.dicksinmyan.us"]

    userpath = os.getcwd()
    user = getpass.getuser()
    passfile = args.pf
    emailfile = args.ef
    encryptedpassword = open(passfile).read()
    encryptedusername = open(emailfile).read()
    RecipientFingerprint = args.rf
    RecipientEmail = args.re
    EmailSubject = args.s
    EmailMessage = args.m

    if platform.system() != "Windows":
        gpg = gnupg.GPG(gnupghome=f"/home/{user}/.gnupg")
    else:
        gpg = gnupg.GPG()

    if args.ae is None:
        SenderFingerprint = str(input("Enter email associated with your public key or key fingerprint (doesn\'t have to be your sending email address): "))
        if SenderFingerprint == "":
            print("ERROR: You didn\'t specified an email, exiting...")
            sys.exit(1)
    else:
        SenderFingerprint = args.ae

    SenderID = SenderFingerprint.replace(" ","")
    pkey = gpg.export_keys(SenderID)
    pubkey = open("publickey.txt", "w")
    pubkey.write(pkey)
    pubkey.close()

    if args.pp is None:
        decryptedpassword = str(gpg.decrypt(encryptedpassword))
        password = decryptedpassword.partition("\n")[0]
        decryptedusername = str(gpg.decrypt(encryptedusername))
    else:
        decryptedpassword = str(gpg.decrypt(encryptedpassword, passphrase=args.pp))
        password = decryptedpassword.partition("\n")[0]
        decryptedusername = str(gpg.decrypt(encryptedusername, passphrase=args.pp))

    username = decryptedusername.partition("\n")[0]
    providername = username.split("@",1)[1]
    TLS_port = args.pt

    if args.ms is None:
        if any(providername in i for i in cockliservers):
            server = "mail.cock.li"
        if providername == ( "disroot.org" or "disroot" ):
            server = "disroot.org"
        elif providername == ( "gmail.com" or "smtp.gmail.com" or "google" or "gmail" ):
            server = "smtp.gmail.com"
            print("\nTIP: You need to add app password from your Google account for this script to work, in case of error visit:\nhttps://support.google.com/accounts/answer/185833?hl=en\n")
        elif providername == ( "posteo.net" or "posteo.de" or "posteo "):
            server = "posteo.de"
        elif providername == ( "startmail.com" or "smtp.startmail.com" or "startmail" ):
            server = "smtp.startmail.com"
        elif providername == ( "yahoo.com" or "smtp.mail.yahoo.com" or "mail.yahoo.com" or "yahoo" ):
            server = "smtp.mail.yahoo.com"
        elif providername == ( "live.com" or "live" or "smtp.live.com" ):
            server = "smtp.live.com"
        elif providername == ( "outlook.com" or "outlook" or "hotmail.com" or "hotmail" ):
            server = "smtp-mail.outlook.com"
            print("\nTIP: You need to add app password from your Microsoft account for this script to work, in case of error visit: \nhttps://support.microsoft.com/en-us/account-billing/using-app-passwords-with-apps-that-don-t-support-two-step-verification-5896ed9b-4263-e681-128a-a6f2979a7944\n")
        else:
            print("\nERROR: Provider not in the list, contact maintainer of this project for adding the provider you use to the list or simply use the --ms command to input the SMTP server manually.")
            sys.exit(1)
    else:
        server = args.ms

    msg = MIMEMultipart()

    if args.at == True:
        Recipient = email(msg, username, gpg, RecipientFingerprint, RecipientEmail, EmailSubject, EmailMessage)
        attachment(userpath, msg)
        authentication(Recipient, server, TLS_port, username, password, msg)
    else:
        Recipient = email(msg, username, gpg, RecipientFingerprint, RecipientEmail, EmailSubject, EmailMessage)
        authentication(Recipient, server, TLS_port, username, password, msg)
    
    os.remove(userpath + "/publickey.txt")

if __name__ == "__main__":
    main()
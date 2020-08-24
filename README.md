# pypgp

**Python script for encrypting messages using local PGP keys and sending them over email using smtp**

This script can be used for email clients that support SMTP protocol for sending emails
### Dependencies
You need python-gnupg package for script to run, install it with:

`sudo pip3 install python-gnupg` or `conda install -c conda-forge python-gnupg` if you are using conda enviroment.
### Preparation
Clone this repo by typing 

`git clone https://codeberg.org/nikolal/pypgp.git` and then change into working folder:

`cd pypgp`

First, you need to type your email and password for that email in two adequate separate .txt files, and script assumes that your PGP keys are associated with that email.

Then you encrypt that two text files with your private keys and remove .txt plaintext files, when you use script it will prompt you for your PGP password for decryption. This is done this way if someone also uses your computer so they can't be able to see your credentials. You do it this way from your CLI:

`gpg -ea -r youremail@domain.com email.txt` and `gpg -ea -r youremail@domain password.txt`

Next step is to remove plaintext versions of your credentials:

`rm -v email.txt password.txt`
### Usage
Thats it, you run script by typing `python3 pypgp.py`
### Optional
You can run script just by typing pypgp in your terminal, just add this line to your .bash_aliases file:
`alias pypgp='python3 /home/$USER/pygpg/pypgp.py'`

If you are using this script on remote server with no display, or OS that works without display you can add these lines in your .bashrc file for GPG to prompt for password in CLI:
<br />
`GPG_TTY=$(tty)
`<br />
`export GPG_TTY`

**Note that this script makes easy for me to send PGP emails and I hope it will help you too. Message is encrypted before sending it to SMTP server so it should be safe. I'm not security or expert just humble privacy advocate, use this script with caution. Any feedback is appreciated.**

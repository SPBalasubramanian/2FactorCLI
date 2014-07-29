# 2 Factor CLI

This is a simple python program to allow you to store and generate time-based
one-time passwords in a GPG encrypted vault.

This allows you to use 2factor to log in without getting out your phone

# Extracting secrets from qrcodes

You can:

 * Use a QR code reader on your phone
 * [zbar](http://zbar.sourceforge.net/) provides zbarimg
 
Once you decode the qr code, it'll be a quasi-url that contains something like

    secret=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890
    
Use ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 as the secret passed to the app


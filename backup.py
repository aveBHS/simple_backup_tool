import smtplib                                     
from datetime import datetime, timedelta
import dropbox
import subprocess
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText               
from email.mime.image import MIMEImage 
import time

#Configuration
product_name = ''     #Product name
dropbox_token = ''    #Dropbox token
dropbox_folder = '/'  #Dropbox folder (/ for root)
smtp_server = ''      #SMTP server of your out mail box
addr_from = ""        #Mail box from             
addr_to   = ""        #Mail box to            
password  = ""        #Password from mail box from
password_length = 16  #Archive password length
lapse = 86400         #Backup lapse (86400 - day)
files_list = [        #List of files for backup
    './' 
]
    
def genPassword(length):
    password = ''
    arr = ['a','b','c','d','e','f',
           'g','h','i','j','k','l',
           'm','n','o','p','r','s',
           't','u','v','x','y','z',
           'A','B','C','D','E','F',
           'G','H','I','J','K','L',
           'M','N','O','P','R','S',
           'T','U','V','X','Y','Z',
           '1','2','3','4','5','6',
           '7','8','9','0']
    for i in range(0, length):
        password += arr[randint(0, len(arr)-1)]
    return password

def genList():
    file_list_str = ''
    for file_name in files_list:
        file_list_str += file_name + ' '
    return file_list_str

while True:   

    password_archive = genPassword(password_length)
    date = datetime.now()
    date_str = (date.strftime("%d.%m.%Y %H:%M"))   
    dropbox_file_name = dropbox_folder + '/backup_' + date.strftime("%d.%m.%Y_%H_%M") + '.zip'

    print('Creating backup...')

    subprocess.call(f'zip -P {password_archive} -r backup.zip ' + genList(), shell=True)

    dbx = dropbox.Dropbox(dropbox_token)   
    with open("backup.zip", "rb") as f:
        dbx.files_upload(f.read(), dropbox_file_name, mute = True)

    msg = MIMEMultipart()                               
    msg['From']    = addr_from                          
    msg['To']      = addr_to                            
    msg['Subject'] = f'{product_name} | Backup {date_str}'             

    expire = (datetime.now() + timedelta(hours=4)).strftime("%d.%m.%Y %H:%M")
    link = dbx.files_get_temporary_link(path=dropbox_file_name).link
    body = f"Backup data of {product_name}\nDate: {date_str}\nTemporary download link (expire in {expire}): {link}\nDropbox url: https://www.dropbox.com/home{dropbox_file_name}\nPassword of archive: {password_archive}\nCopyright 2020 BHS Studio"
    msg.attach(MIMEText(body, 'plain'))                   
    server = smtplib.SMTP(smtp_server, 25)                     
    server.starttls()                          
    server.login(addr_from, password)                 
    server.send_message(msg)                            
    server.quit()   
            
    if(lapse == -1):
        print(f'Complate!')   
        break     
    else:
        print(f'Complate! Next backup in {lapse} sec.')   
        time.sleep(lapse)             

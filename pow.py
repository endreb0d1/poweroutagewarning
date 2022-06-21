import requests
from bs4 import BeautifulSoup
import smtplib
import time

new_towns = ""

towns = new_towns

while True:
    try:
        # get last maintenance link (insert area relevant to you, eg. Subotica, Zrenjanin, Ruma...)
        url = "http://www.elektrovojvodina.rs/sl/mediji/ED-Pancevo12"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html5lib")

        # get affected new_towns and streets from table
        url = "http://www.elektrovojvodina.rs/"
        r = requests.get(url + soup.select_one("a[href*=Dana]")["href"])
        soup = BeautifulSoup(r.content, "html5lib")

        table = soup.find("table")
        
        new_towns = ""
        
        for row in table.findAll("p"):
            row = row.text
            
            # replace unnecessary tabs and spaces
            row = row.replace("\xa0", " ")
            row = row.replace("\t", "")
            row = row.replace("\n", "")
            
            # replace unnecessary numbers
            if len(row) < 3:
                row = ""
            
            new_towns += (row + "\n")
        
        # insert relevant town name    
        town = "your_town"

        # send email notification
        if town in new_towns and new_towns != towns:
            s = smtplib.SMTP("smtp.gmail.com", 587)
            s.starttls()
            s.login("sender_email_id@gmail.com", "sender_email_password")
            sender = "sender_email_id@gmail.com"
            receiver = "receiver_email_id@gmail.com"
            subject = "Obavestenje o iskljucenju struje"
            text = new_towns
            message = f"Subject: {subject}\n\n{text}"
            s.sendmail(sender, receiver, message.encode("utf-8"))
            s.quit()

            towns = new_towns

    except:
        pass
        
    # check for changes every 8 hours    
    time.sleep(28800)

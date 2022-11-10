import requests
import json
from bs4 import BeautifulSoup
import time

reset_signal = 0
old_message = "" 
message_backup = ""

TOKEN = "5741061538:AAFBQz2VitaWwuTX-LJATOaolmFq3Wc3J4E"
chat_id = "866992945"


while True:

    #print("Getting webstite")
    opera = requests.get('https://biletinial.com/dynamic/getetkinliktakvimi/713?cityId=3')

    if opera:
        new_message = ""
        #print("Website is on \n")
    else:
        new_message = "!!!ERRORRR"
        #print("!!ERROR")
        
    #check = b'Tosca' in opera.content

    soup = BeautifulSoup(opera.text, "html.parser")

    body = soup.find("tbody")
    containers = body.find_all("tr")

    for container in containers:
        date = container.find("td",{"class":"baslikAraYN"}).text
        name = container.find("a",{"class":"info-label"}).text
        

        name = " ".join(name.split())
        date  = " ".join(date.split())
        #print(date + " || " + name)
        new_message += date + " || " + name + "\n \n"
        
    message_backup = new_message

    if new_message != old_message and reset_signal:
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={new_message}"
        requests.get(url).json() # this sends the new_message
        
        if old_message in new_message:  # yeni mesajdan eskisi siliniyor
            
            new_message = new_message.replace(old_message,"")
            new_message = "!!NEW \n" + new_message
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={new_message}"
            requests.get(url).json() # this sends the new_message
            
        elif new_message in old_message:
            
            old_message = old_message.replace(new_message,"")
            old_message = "!!Deleted \n" + old_message
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={old_message}"
            requests.get(url).json() # this sends the new_message            
    """
    else:
        a = "no change"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={a}"
        requests.get(url).json() # this sends the new_message
    
    """
    old_message = message_backup
    new_message  = message_backup
        
    reset_signal = 1
    time.sleep(300)

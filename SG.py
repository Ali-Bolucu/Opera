import requests
import json
from bs4 import BeautifulSoup
import time


new_message = "" # aslında eskisi
message_change = ""

TOKEN = "5741061538:AAFBQz2VitaWwuTX-LJATOaolmFq3Wc3J4E"
chat_id = "866992945"



#print("Getting webstite")
opera = requests.get('https://biletinial.com/dynamic/getetkinliktakvimi/713?cityId=3')

if opera:
    message = ""
    print("Website is on \n")
else:
    message = "!!!ERRORRR"
    print("!!ERROR")
    
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
    message += date + " || " + name + "\n \n"

if message != new_message:
    
    message_change = message
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json() # this sends the message
    
    if new_message in message:  # yeni mesajdan eskisi siliniyor
        
        message = message.replace(new_message,"")
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(url).json() # this sends the message
        
    elif message in new_message:
        
        new_message = new_message.replace(message,"")
        new_message = "!!Deleted \n" + new_message
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={new_message}"
        requests.get(url).json() # this sends the message            
    
    new_message = message_change
    message  = message_change
else:
    a = "no change"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={a}"
    requests.get(url).json() # this sends the message

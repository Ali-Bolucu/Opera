import requests
import json
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
import re

class bot(object):      
    def __init__(self) -> None:
        
        self.bResetSignal = bool(False)
        self.URL_RESPONSE = str("Initialized")
        self.text = str("Initialized")
        self.tickets = str("Initialized")  
        self.stored_tickets = str("stored_tickets")
        self.current_tickets = str("")
    
        self.API_TOKEN = "5741061538:AAFBQz2VitaWwuTX-LJATOaolmFq3Wc3J4E"
        self.CHAT_ID = "866992945"
        self.TICKET_URL = 'https://biletinial.com/dynamic/getetkinliktakvimi/713?cityId=3'
    
    def BOT_URL(self, text) -> str:
        return f"https://api.telegram.org/bot{self.API_TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={text}"
    
    def start_message(self) -> None:
        self.text = "Start working"
        requests.get(self.BOT_URL(self.text)).json() # this sends the new_message
        
    def url_status(self) -> bool:
        self.URL_RESPONSE = requests.get(self.TICKET_URL, headers={'User-Agent': str(UserAgent().random)})
        
        if self.URL_RESPONSE.status_code != 200:
            requests.get(self.BOT_URL(self.text)).json()
            return False
        return True
    
    def url_parser(self) -> None:
        URL_CONTENT = self.URL_RESPONSE.text
        
        html_content = BeautifulSoup(URL_CONTENT, "html.parser")
        html_body = html_content.find("tbody")
        containers = html_body.find_all("tr")
        
        for container in containers:
            date = container.find("td",{"class":"baslikAraYN"}).text
            name = container.find("a",{"class":"info-label"}).text
                

            name = " ".join(name.split())
            date  = " ".join(date.split())
            #print(date + " || " + name)
            
            self.current_tickets += date + "\n" + name + "\n \n"
            self.current_tickets = re.sub(r'[&%+-]', '', self.current_tickets)
            
    
    def send_tickets(self) -> None:
        if self.current_tickets != self.stored_tickets and self.bResetSignal:
            requests.get(self.BOT_URL(self.current_tickets)).json() # Sends all tickets
            
            if self.stored_tickets in self.current_tickets:  # Sends only new tickets
                requests.get(self.BOT_URL(str( "NEW !!\n" + self.current_tickets.replace(self.stored_tickets, "")))).json()
            elif self.current_tickets in self.stored_tickets:  # Sends the deleted tickets
                requests.get(self.BOT_URL(str( "Deleted !!\n" + self.stored_tickets.replace(self.current_tickets, "")))).json()
                
            time.sleep(3600) # if threre is a change, wait 1 hour before checking again
        
        self.stored_tickets = self.current_tickets
        self.current_tickets = str("") # Empty the string
        self.bResetSignal = True 
        time.sleep(150) # checks the website every 2.5 minute
        
                
#----------------------------------------------------------------------------------------------------------------------------------

def main() -> None:
    botobj = bot()
    botobj.start_message()
    
    while True:
        if botobj.url_status():
            botobj.url_parser()
            botobj.send_tickets()
        else:
            time.sleep(3600) # if the website gives error, wait 1 hour
    
if __name__ == "__main__" :
    main()

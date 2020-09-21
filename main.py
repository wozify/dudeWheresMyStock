import re
import time
import smtplib
import requests
from datetime import datetime 
from bs4 import BeautifulSoup

def stock_check(url):
    """Checks url for 'sold out!' substring in buy-now-bar-con"""
    soup = BeautifulSoup(url.content, "html.parser") #Need to use lxml parser
    stock = soup.find("div", "buy-now-bar-con") #Check the html tags for sold out/coming soon info.
    stock_status = re.findall(r"sold out!", str(stock)) #Returns list of captured substring if exists.
    return stock_status # returns "sold out!" from soup string.

def send_email(address, password, message):
    """Send an e-mail to yourself!"""
    server = smtplib.SMTP("smtp.gmail.com", 587) #e-mail server
    server.ehlo()
    server.starttls()
    server.login(address,password) #login
    message = str(message) #message to email yourself
    server.sendmail(address,address,message) #send the email through dedicated server
    return

def stock_check_listener(url, address, password, run_hours):
    """Periodically checks stock information."""
    listen = True # listen boolean
    start = datetime.now() # start time
    while(listen): #while listen = True, run loop
        if "sold out!" in stock_check(url): #check page
            now = datetime.now()
            print(str(now) + ": Not in stock.")
        else:
            message = str(now) + ": NOW IN STOCK!"
            print(message)
            send_email(address, password, message)
            listen = False

        duration = (now - start)
        seconds = duration.total_seconds()
        hours = int(seconds/3600)
        if hours >= run_hours: #check run time
            print("Finished.")
            listen = False

        time.sleep(30*60) #Wait N minutes to check again.    
    return

if __name__=="__main__":

    #Set url and userAgent header for javascript issues.
    page = "https://shop.bitmain.com/antminer_s9_asic_bitcoin_miner.htm"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html'}

    #URL request.
    url = requests.get(url=page,
                       headers=headers)

    #Run listener to stream stock checks.
    address = "user@gmail.com" #your email
    password = "user.password" #your email password
    stock_check_listener(url=url,
                         address=address,
                         password=password,
                         run_hours=1) 

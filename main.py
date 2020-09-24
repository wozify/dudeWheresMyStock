import requests
from bs4 import BeautifulSoup
import time
import smtplib

while True:
    url = "https://www.newegg.com/p/pl?N=100007709%20601357247"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    # if the number of times the word "Google" occurs on the page is less than 1,
    if str(soup).find("Add to cart ") == -1:
        time.sleep(60)
        continue

    else:
        msg = 'Subject: Guess What? 3080s are back in stock on Newegg!'
        fromaddr = 'YOUR_EMAIL_ADDRESS'
        toaddrs = ['YOUR_EMAIL_ADDRESS']

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("YOUR_EMAIL_ADDRESS", "YOUR_PASSWORD")

        # Print the email's contents
        print('From: ' + fromaddr)
        print('To: ' + str(toaddrs))
        print('Message: ' + msg)

        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()

        break

import requests
from bs4 import BeautifulSoup
import smtplib
from re import sub
from decimal import Decimal


URL = "https://www.amazon.com/dp/B00FSB799Q/ref=psdc_173565_t3_B00FSB79KU"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}


def get_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    soup1 = BeautifulSoup(soup.prettify(), "html.parser")
    title = soup1.find(id="productTitle").get_text()
    price = soup1.find(id="priceblock_ourprice").get_text()
    # Price comes back as string, use RegExp and Decimal to convert to number
    stripped_title = title.strip()
    converted_price = Decimal(sub(r"[^\d.]", "", price))
    if converted_price < 1000:
        send_mail(stripped_title)


def send_mail(title):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # Insert login credentials below
    server.login("email@email.com", "password")

    subject = f"Price fell down on {title}"
    body = f"Check the amazon link {URL}"
    msg = f"Subject: {subject}\n\n{body}"
    # Enter to, from below
    server.sendmail("email@email.com", "email@email.com", msg)
    print("Email has been sent")
    server.quit()


get_price()

import requests
from bs4 import BeautifulSoup
import smtplib
from re import sub
from decimal import Decimal

# Insert Amazon urls and prices of products being tracked as shown below
products = [
    {
        "url": "https://www.amazon.com/dp/B00FSB799Q/ref=psdc_173565_t3_B00FSB79KU",
        "price": 1000,
    },
    {
        "url": "https://www.amazon.com/Sony-a7R-Mirrorless-Camera-Interchangeable/dp/B076TGDHPT",
        "price": 2500,
    },
]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}


def get_price(products):
    for product in products:
        page = requests.get(product["url"], headers=headers)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        soup1 = BeautifulSoup(soup.prettify(), "html.parser")
        title = soup1.find(id="productTitle").get_text()
        price = soup1.find(id="priceblock_ourprice").get_text()
        stripped_title = title.strip()
        # Price comes back as string, use RegExp and Decimal to convert to number
        converted_price = Decimal(sub(r"[^\d.]", "", price))
        print(converted_price)
        if converted_price < product["price"]:
            send_mail(stripped_title, product["url"])


def send_mail(title, url):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # Insert login credentials below
    server.login("email@email.com", "password")

    subject = f"Price is down - {title}"
    body = f"{url}"
    msg = f"Subject: {subject}\n\n{body}"
    # Enter to, from below
    server.sendmail("to@email.com", "from@email.com", msg)
    print("Email has been sent")
    server.quit()


get_price(products)

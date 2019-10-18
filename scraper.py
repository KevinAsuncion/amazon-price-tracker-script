import requests
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal

URL = "https://www.amazon.com/dp/B00FSB799Q/ref=psdc_173565_t3_B00FSB79KU"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")
soup1 = BeautifulSoup(soup.prettify(), "html.parser")

title = soup1.find(id="productTitle").get_text()
price = soup1.find(id="priceblock_ourprice").get_text()
# Price comes back as string, use RegExp and Decimal to convert to float
converted_price = Decimal(sub(r"[^\d.]", "", price))
print(converted_price)


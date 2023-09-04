import os

import requests
from bs4 import BeautifulSoup
import smtplib
import lxml
from dotenv import load_dotenv

load_dotenv()

password = os.getenv('my_password')
my_email = os.getenv('my_email')
receiver = os.getenv('receiver')

url = 'https://www.amazon.com/adidas-Ownthegame-Basketball-Black-Carbon/dp/B08N5P7F3J/ref=sr_1_6?crid=1SX359GXNO1QP&keywords=adidas+shoes+men&qid=1690028109&sprefix=adidas%2Caps%2C239&sr=8-6'
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"
}
response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, 'lxml')
# print(soup.prettify())

price = soup.find(class_='a-offscreen').getText()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)

title = soup.find(id= "productTitle").getText().strip()
target_price = 200
if price_as_float <= target_price:
    message = f"{title} is now ${target_price}"
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        result = connection.login(my_email, password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=receiver,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )

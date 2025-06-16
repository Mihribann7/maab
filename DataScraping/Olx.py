import requests
from bs4 import BeautifulSoup

url = "https://www.olx.uz/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

ads = soup.find_all("div", class_="css-1sw7q4x")

for ad in ads:
    title_tag = ad.find("a", class_="css-1tqlkj0")
    title = title_tag.text.strip() if title_tag else "N/A"

    link = "https://www.olx.uz" + title_tag['href'] if title_tag else "N/A"

    price_tag = ad.find("p", class_="css-1vhm4ri")
    price = price_tag.text.strip() if price_tag else "N/A"

    address_tag = ad.find("p", class_="css-1pzx3wn")
    address = address_tag.text.strip() if address_tag else "N/A"

    date_tag = ad.find("p", class_="css-1uf1vew")
    date_posted = date_tag.text.strip() if date_tag else "N/A"

    print(f"Title: {title}")
    print(f"Price: {price}")
    print(f"Address: {address}")
    print(f"Date Posted: {date_posted}")
    print(f"Link: {link}")
    print("=====================================\n")

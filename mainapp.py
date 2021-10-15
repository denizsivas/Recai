import requests
from bs4 import BeautifulSoup

url = 'https://www.hepsiburada.com/dell-ultrasharp-u2421he-23-8-60-hz-8-ms-hdmi-dp-type-c-full-hd-ips-led-monitor-p-HBV00001AVZ5I'
header_param = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0'}
page = requests.get(url, headers=header_param)
print(page.status_code)
soup = BeautifulSoup(page.text, 'html.parser')
product_name = soup.find_all("h1", {"id": "product-name"})
product_name_raw = product_name[0].contents[0].text
product_name_stripped = product_name_raw.split('\n')
product_name_stripped = product_name_stripped[1].lstrip()
product_price = soup.find_all("span", {"id": "offering-price"})
price_raw = product_price[0].text
price_stripped = price_raw.split('\n')
price_stripped = price_stripped[1]
print(product_name_stripped)
print(price_stripped)
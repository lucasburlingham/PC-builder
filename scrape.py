from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore
import sqlite3
from datetime import datetime
import sys

# Get the title and price of a product on Amazon
class AmazonProduct:
	def __init__(self, url):
		self.url = url
		self.soup = self.get_soup()
		self.title = self.get_title()
		self.price = self.get_price()

	def get_soup(self):
		HEADERS = ({'User-Agent':
					'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
					'Accept-Language': 'en-US, en;q=0.5'})
		webpage = requests.get(self.url, headers=HEADERS)
		return BeautifulSoup(webpage.content, "lxml")

	def get_title(self):
		try:
			title = self.soup.find("span", attrs={"id":'productTitle'})
			return title.string.strip()
		except AttributeError:
			return ""

	def get_price(self):
		try:
			price_whole = str(self.soup.find("span", attrs={'class':'a-price-whole'}).text)
			price_fraction = str(self.soup.find("span", attrs={'class':'a-price-fraction'}).text)
			price = price_whole + price_fraction
			return price
		except AttributeError:
			return ""

class EbayProduct:
	def __init__(self, url):
		self.url = url
		self.soup = self.get_soup()
		self.title = self.get_title()
		self.price = self.get_price()

	def get_soup(self):
		HEADERS = ({'User-Agent':
					'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
					'Accept-Language': 'en-US, en;q=0.5'})
		webpage = requests.get(self.url, headers=HEADERS)
		return BeautifulSoup(webpage.content, "lxml")

	def get_title(self):
		try:
			title = self.soup.find("h1", attrs={"id":'mainContent'})
			title = self.soup.find("h1", attrs={"class":'x-item-title__mainTitle'})	
			title = str(title.find("span", attrs={"class":'ux-textspans'}).text)
			return title.strip()
		except AttributeError:
			return ""

	def get_price(self):
		try:
			price = self.soup.find("div", attrs={'class':'x-bin-price__content'})
			price = str(price.find("span", attrs={'class':'ux-textspans'}).text)
			# Remove US $ from the price
			price = price.replace("US $", "")
			return price.strip()
		except AttributeError:
			return ""

class NewEggProduct:
	def __init__(self, url):
		self.url = url
		self.soup = self.get_soup()
		self.title = self.get_title()
		self.price = self.get_price()
  
	def get_soup(self):
		HEADERS = ({'User-Agent':
					'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
					'Accept-Language': 'en-US, en;q=0.5'})
		webpage = requests.get(self.url, headers=HEADERS)
		return BeautifulSoup(webpage.content, "lxml")

	def get_title(self):
		try:
			title = self.soup.find("h1", attrs={"class":'product-title'})
			return title.string.strip()
		except AttributeError:
			return ""

	def get_price(self):
		try:
			price = self.soup.find("li", attrs={'class':'price-current'})
			# string will look like <li class="price-current"><span class="price-current-label"></span>$<strong>397</strong><sup>.85</sup></li>
			# parse this out to be whole dollars and fraction cents
			price_whole = str(price.find("strong").text)
			price_fraction = str(price.find("sup").text)
			price = price_whole + price_fraction
			return price.strip()
		except AttributeError:
			return ""


# Get list of URL's from a string passed as the 1st arg and scrape the data from the URL's
# Save it to sqlite database stored in the same directory with the name 'scraped_products.db'
# The database should look like this: 
# +----+-----------------+-----------------+-----------------+---------------+
# | id | title           | price           | url             | Date Scraped  |
# +----+-----------------+-----------------+-----------------+---------------+

def parse_url(url_string):
	urls = []
	for url in url_string:
		if(url.startswith("https://www.amazon.com")):
			urls.append(AmazonProduct(url))
		elif(url.startswith("https://www.ebay.com")):
			urls.append(EbayProduct(url))
		elif(url.startswith("https://www.newegg.com")):
			urls.append(NewEggProduct(url))   
	return urls


def main():
    
    
	if len(sys.argv) < 2:
		print("Error (1): Please pass in a list of URL's to scrape!")
		# Exit and spit out an error code to the shell
		sys.exit(1)
 
	print("url_string: ", sys.argv[1:])
	# Create a database in the same directory
	db = sqlite3.connect("scraped_products.db")
	db = db.cursor()
	# Create a table to store the data
	db.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, title TEXT, price TEXT, url TEXT, epoch_scraped TEXT)")
	print("DB Ready")
	
	url_string = sys.argv[1:]

	print("Parsing URL's")
	urls = parse_url(url_string)
	print("URL's parsed")

	# Print the data nicely
	# Get the length of the longest element in each column and use that to format the output
	for url in urls:
		epoch_time = datetime.now().strftime('%s')
		print(url.title, ",", url.price, ",", url.url, ",", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		db.execute("INSERT INTO products (title, price, url, epoch_scraped) VALUES (?, ?, ?, ?)", (url.title, url.price, url.url, epoch_time))

	# Commit the changes to the database
	db.connection.commit()
	db.close()
		
main()
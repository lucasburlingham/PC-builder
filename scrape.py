from bs4 import BeautifulSoup
import requests
import sqlite3
import time
# import sys
import json
import os


# Create a database to store the scraped data
# The database should look like this:
# +----+-----------------+-----------------+-----------------+---------------+---------------+---------------+
# | id | title           | price           | url             | Date Scraped  | json          | image_url     |
# +----+-----------------+-----------------+-----------------+---------------+---------------+---------------+
db = sqlite3.connect("storage.db")
db = db.cursor()
# Create a table to store the data
db.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, title TEXT, price TEXT, url TEXT, epoch_scraped INTEGER, json TEXT, image_url TEXT)")

# Create a table to store the build configurations
# The database should look like this:
# +----+-----------------+-----------------+-----------------+
# | id | title           | config          | date_added      |
# +----+-----------------+-----------------+-----------------+

# Create a table to store the build configurations
db.execute("CREATE TABLE IF NOT EXISTS build_config (id INTEGER PRIMARY KEY, title TEXT, config TEXT, date_added INTEGER)")
db.connection.commit()

# Get the title and price of a product on Amazon
class AmazonProduct:
	def __init__(self, url):
		self.url = url
		self.soup = self.get_soup()
		self.title = self.get_title()
		self.price = self.get_price()
		self.image = self.get_image()
		# Encode the data as a JSON string to replace the URL in the build_config db		
		self.json = '{"title": "' + self.title + '", "price": "' + self.price + '", "url": "' + self.url + '", "epoch_scraped": "' + str(epoch_time()) + '", "image":"' + self.image + '"}'

	def get_soup(self):
		HEADERS = ({'User-Agent':
					'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
					'Accept-Language': 'en-US, en;q=0.5'})
		# Try this from https://yaleman.org/post/2018/2018-11-06-speeding-up-beautifulsoup-with-large-xml-files/
		webpage = requests.get(self.url, headers=HEADERS)
		webpage = webpage.content.decode('utf-8')
		return BeautifulSoup(webpage, "lxml")

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

	def get_image(self):
		try:
			image = self.soup.find("img", attrs={'id':'landingImage'})
			if image:
				return image['src']
			else:
				return ""
		except AttributeError:
			return ""

class EbayProduct:
	def __init__(self, url):
		self.url = url
		self.soup = self.get_soup()
		self.title = self.get_title()
		self.price = self.get_price()
		self.image = self.get_image()
		# Encode the data as a JSON string to replace the URL in the build_config db		
		self.json = '{"title": "' + self.title + '", "price": "' + self.price + '", "url": "' + self.url + '", "epoch_scraped": "' + str(epoch_time()) + '", "image":"' + self.image + '"}'

	def get_soup(self):
		HEADERS = ({'User-Agent':
					'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
					'Accept-Language': 'en-US, en;q=0.5'})
		webpage = requests.get(self.url, headers=HEADERS)
		webpage = webpage.content.decode('utf-8')
		return BeautifulSoup(webpage, "lxml")

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

	def get_image(self):
		try:
			image = self.soup.find("div", attrs={'class':'ux-image-carousel-item image-treatment image'})
			image = image.find("img")
			return image['src']
		except AttributeError:
			return ""

class NewEggProduct:
   
	def __init__(self, url):
		self.url = url
		self.soup = self.get_soup()
		self.title = self.get_title()
		self.price = self.get_price()
		self.image = self.get_image()
		# Encode the data as a JSON string to replace the URL in the build_config db		
		self.json = '{"title": "' + self.title + '", "price": "' + self.price + '", "url": "' + self.url + '", "epoch_scraped": "' + str(epoch_time()) + '", "image":"' + self.image + '"}'
  
	def get_soup(self):
		HEADERS = ({'User-Agent':
					'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
					'Accept-Language': 'en-US, en;q=0.5'})
		webpage = requests.get(self.url, headers=HEADERS)
		webpage = webpage.content.decode('utf-8')
		return BeautifulSoup(webpage, "lxml")

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

	def get_image(self):
		try:
			image = self.soup.find("img", attrs={'class':'product-view-img-original'})
			return image['src']
		except AttributeError:
			return ""

class MicroCenterProduct:
	def __init__(self, url):
		self.url = url
		self.soup = self.get_soup()
		self.title = self.get_title()
		self.price = self.get_price()
		self.image = self.get_image()
		# Encode the data as a JSON string to replace the URL in the build_config db		
		self.json = '{"title": "' + self.title + '", "price": "' + self.price + '", "url": "' + self.url + '", "epoch_scraped": "' + str(epoch_time()) + '"}'

	def get_soup(self):
		HEADERS = ({'User-Agent':
					'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
					'Accept-Language': 'en-US, en;q=0.5'})
		webpage = requests.get(self.url, headers=HEADERS)
		webpage = webpage.content.decode('utf-8')
		return BeautifulSoup(webpage, "lxml")

	def get_title(self):
		# Get the 6 digit SKU from the URL https://www.microcenter.com/product/683068/intel-xeon-w5-3435x-sapphire-rapids-310ghz-sixteen-core-lga-4677-boxed-processor-heatsink-not-included
		sku = self.url.split("/")[-2]
		try:
			title = self.soup.find("span", attrs={"class":'ProductLink_{0}'.format(sku)}).text
			return title.strip()
		except AttributeError:
			return ""

	def get_price(self):
		try:
			price = self.soup.find("span", attrs={'id':'pricing'})
			# <span><span id="pricing" content="1,599.99"></span><sup class="dollar2022">$</sup>1,599.<sup class="cent2022">99</sup></span>
			price = price['content']
			# Remove commas from the price
			price = price.replace(",", "")
			return price.strip()
		except AttributeError:
			return ""

	def get_image(self):
		try:
			image = self.soup.find("img", attrs={'class':'productImageZoom'})
			return image['src']
		except AttributeError:
			return ""

class BestBuyProduct:
	def __init__(self, url):
		self.url = url
		self.soup = self.get_soup()
		self.title = self.get_title()
		self.price = self.get_price()
		self.image = self.get_image()
		# Encode the data as a JSON string to replace the URL in the build_config db		
		self.json = '{"title": "' + self.title + '", "price": "' + self.price + '", "url": "' + self.url + '", "epoch_scraped": "' + str(epoch_time()) + '"}'

	def get_soup(self):
		HEADERS = ({'User-Agent':
					'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
					'Accept-Language': 'en-US, en;q=0.5'})
		webpage = requests.get(self.url, headers=HEADERS)
		webpage = webpage.content.decode('utf-8')
		return BeautifulSoup(webpage, "lxml")

	def get_title(self):
		try:
			title = self.soup.find("div", attrs={"itemprop":'name'})
			title = title.find("h1").text
			return title.strip()
		except AttributeError:
			return ""

	def get_price(self):
		try:
			price = self.soup.find("div", attrs={'data-testid':'customer-price'})
			price = price.find("span").text
			# Remove $ from the price
			price = price.replace("$", "")
			return price.strip()
		except AttributeError:
			return ""

	def get_image(self):
		try:
			image = self.soup.find("img", attrs={'class':'primary-image'})
			image = image.find("img")
			return image['src']
		except AttributeError:
			return ""

class IntegratedProduct:
	def __init__(self, title, price, url, json, image):
			self.title = title
			self.price = price
			self.url = url
			self.json = json
			self.image = image
    
def epoch_time():
	return str(time.time())[:10]

def parse_url(url):
	if(url.startswith("https://www.amazon.com")):
		print("Parsing Amazon URL: " + url)
		url = AmazonProduct(url)
	elif(url.startswith("https://www.ebay.com")):
		print("Parsing Ebay URL: " + url)
		url = EbayProduct(url)
	elif(url.startswith("https://www.newegg.com")):
		print("Parsing NewEgg URL: " + url)
		url = NewEggProduct(url)
	elif(url.startswith("https://www.bestbuy.com")):
		print("Parsing BestBuy URL: " + url)
		url = BestBuyProduct(url)
	elif(url.startswith("https://www.microcenter.com")):
		print("Parsing MicroCenter URL: " + url)
		url = MicroCenterProduct(url)
	elif(url.startswith("Integrated")):
		print("Product is integrated. Not scraping.")
		# If the product is integrated, return the JSON string but use a class so we can reference it normally
		epoch_now = str(epoch_time())
		url = IntegratedProduct("Integrated", 0.00, "#integrated_warning", '{"title": "Integrated", "price": "0.00", "url": "#integrated_warning", "epoch_scraped": "' + epoch_now + '"}', "https://placehold.co/600x400?text=Integrated+Product")
	else:
		print("Invalid URL: " + url)

	epoch_now = str(epoch_time())
	# Add product to the database
	db.execute("INSERT INTO products (title, price, url, epoch_scraped, json, image_url) VALUES (?, ?, ?, ?, ?, ?)", (url.title, url.price, url.url, epoch_now, url.json, url.image))
	db.connection.commit()

	return url


def main():
    # Start the timer
	start_time = epoch_time()
    
    
	# Get the JSON from all the .json files in pc_blobs
	config_array = []
	for filename in os.listdir('pc_blobs'):
		if filename.endswith('.json'):
			with open('pc_blobs/' + filename, 'r') as f:
				config_array.append(json.load(f))

    
	for build_configuration in config_array:
    #  Loop thorugh the build configuration and get each url. Replace the url with the JSON string containing the title, price, url, and epoch_scraped
		for key, value in build_configuration['config'].items():
			if key == 'storage':
				for storage in value:
					# print("Parsing URL: " + storage['url'] + " for " + key)
					storage['url'] = parse_url(storage['url']).json
			elif key == 'other':
				for other in value:
					# print("Parsing URL: " + other['url'] + " for " + key)
					other['url'] = parse_url(other['url']).json
			else:
				# print("Parsing URL: " + value + " for " + key)
				build_configuration['config'][key] = parse_url(value).json

		# Check if the build configuration is already in the build_config table
		db.execute("SELECT * FROM build_config WHERE title = ?", (build_configuration['title'],))
		if db.fetchone() is None:
			# If the build configuration is not in the build_config table, add it
			db.execute("INSERT INTO build_config (title, config, date_added) VALUES (?, ?, ?)", (build_configuration['title'], str(build_configuration), str(epoch_time())))
			db.connection.commit()
		else:
			# If the build configuration is in the build_config table, update it
			# Convert the build configuration to a string before updating the database so we don't get a bunch of escaped quotes
			db.execute("UPDATE build_config SET config = ? WHERE title = ?", (str(build_configuration), build_configuration['title']))
			db.connection.commit()

		# Print the build configuration
		print(build_configuration)
  
  
	# Commit the changes to the database
	db.connection.commit()
	# Close the database connection
	db.connection.close()
	# Print the time it took to run the script and get the first 3 characters of the time
	print("Scraping completed in " + str(float(epoch_time()) - float(start_time))[:3] + " seconds.")
	
 
main()
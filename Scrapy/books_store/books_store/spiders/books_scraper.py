import scrapy
import sys
sys.path.append("../")
from ..items import BooksStoreItem

class BooksSpider(scrapy.Spider):
	# you must have the following two class variables: name and start_urls. Just as is
	# start_urls must be a list even if we have one website to scrape
	name = "books"
	page_number = 1
	start_urls = [
	"http://books.toscrape.com/catalogue/category/books_1/page-{}.html".format(page_number)
	]
	# name the function as parse and it should have response parameter
	# response will hold the entire source code for the page
	def parse(self, response):

		items = BooksStoreItem()
		all_books_cards = response.css(".col-lg-3")
		for card in all_books_cards:
			titles = card.css("h3 a").xpath("@title")[0].extract()
			prices = card.css("div.product_price p.price_color::text")[0].extract()
			availability = " ".join(card.css("div.product_price p.instock::text")[1].extract().split())
			# yield - think of it as return but not really
			# yield is usually used with a generator - spider uses a generator behind the scenes 

			items["titles"] = titles
			items["prices"] = prices
			items["availability"] = availability

			yield items

		# next_page = response.css(".next a::attr(href)").get()
		BooksSpider.page_number = BooksSpider.page_number + 1
		next_page = "http://books.toscrape.com/catalogue/category/books_1/page-{}.html".format(BooksSpider.page_number)
		if next_page <=50: #something not right here
			yield response.follow(next_page,callback=self.parse)


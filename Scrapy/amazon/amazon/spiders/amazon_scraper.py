import scrapy
from ..items import AmazonItem
import re


class AmazonSpider(scrapy.Spider):
	name = "amazon"
	page_number = 1
	start_urls = [
	"https://www.amazon.com/s?rh=n%3A565108%2Cp_72%3A4-&pf_rd_i=565108&pf_rd_p=b2e34a42-7eb2-50c2-8561-292e13c797df&pf_rd_r=YGEP7PPPWGPAKP9D13QK&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&ref=Oct_s9_apbd_otopr_hd_bw_b2N0e_S"
	]
	

	# custom_proxy = "http://35.169.156.54:3128"
	# def start_request(self):
	# 	for url in self.start_urls:
	# 		request = scrapy.Request(url,callback=self.parse)
	# 		request.meta["proxy"] = self.custom_proxy
	# 		yield request

	def parse(self, response):
		item = AmazonItem()
		all_cards = response.css("div.sg-col-4-of-24")#.css("h2").css("span::text").extract()
		# print(all_cards)
		for index,card in enumerate(all_cards):
			# print(index)
			product_asin = card.css("div.sg-col-4-of-24::attr(data-asin)").extract()
			if not product_asin:
				continue
			product_name = card.css("h2 span::text").extract()
			print(100*"---")
			stars_raw, product_reviews = card.css("div.a-row span a span::text").extract()
			product_stars = stars_raw.split(" ")[0]
			product_price = card.css("div.a-row span.a-price span.a-offscreen").css("::text").extract()
			# 	product_name = card.css("h2").css("span::text").extract()
			# 	print(index,product_name)
			# for index,card in enumerate(all_cards):

			# 	product_asin = card.css("span::attr(name)").extract()

			# 	if not product_asin:
			# 		continue

			# 	product_name = card.css("h2::attr(data-attribute)").extract()
			# 	product_stars = card.css("span.a-icon-alt::text").extract()
			# 	product_stars = re.findall("(\d*\.?\d+)",product_stars[0])[0]
			# 	product_reviews = card.css("span+ .a-text-normal").css("::text").extract()
			# 	product_price = card.css(".a-spacing-mini .a-spacing-none:nth-child(1) .a-text-normal span")\
			# 	.css("::text").extract_first()
			# 	image_link  = card.css(".cfMarker::attr(src)").extract()

			item["product_asin"] = product_asin
			item["product_name"] = product_name
			item["product_stars"] = product_stars
			item["product_reviews"] = product_reviews
			item["product_price"] = product_price
			# 	item["image_link"] = image_link
	 			
			yield item
		print(100*"#",AmazonSpider.page_number)
		next_page = "https://www.amazon.com/s?i=computers&rh=n%3A565108%2Cp_72%3A1248879011&page="+str(AmazonSpider.page_number)+"&pf_rd_i=565108&pf_rd_p=b2e34a42-7eb2-50c2-8561-292e13c797df&pf_rd_r=YGEP7PPPWGPAKP9D13QK&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&qid=1599243327&ref=sr_pg_"+str(AmazonSpider.page_number)
	# 	next_page = "https://www.amazon.com/Laptops-Computers-Tablets/s?rh=n%3A565108&page={}"\
	# .format(AmazonSpider.page_number)
		AmazonSpider.page_number = AmazonSpider.page_number + 1
		if AmazonSpider.page_number <= 3:
			yield response.follow(next_page,callback=self.parse)
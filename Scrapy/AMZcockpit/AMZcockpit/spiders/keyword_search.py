# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import AmzcockpitItem

class KeywordSearchSpider(scrapy.Spider):
    name = 'keyword'
    allowed_domains = ['amazon.co.uk']
    page_number = 1
    seo_overall = 0
    ppc_overall = 0
    def __init__(self,keyword,asin,**kwargs):
        super().__init__(**kwargs)
        self.keyword = keyword
        self.query = "https://www.amazon.co.uk/s?k={}&ref=nb_sb_noss"
        self.found = False
        self.asin = asin
        self.search_url = self.query.format(self.keyword)
        self.sponsored = False
        self.market_place = "https://www.amazon.co.uk/"
        print(100*"#")
        print(self.search_url)
        print(100*"#")
    # Send a request to the market place url eg https://www.amazon.co.uk/
    # send the result to the parse_index function
    def start_requests(self):
        yield Request(self.market_place, callback=self.parse_index)
    # Send request to market place to conduct a search of keyword
    # eg https://www.amazon.co.uk/s?k=laptop&ref=nb_sb_noss for laptop keyword
    # send the result into the parse function below
    def parse_index(self, response):
        yield Request(self.search_url)
    # The following function gets the page source for the search results
    def parse(self, response):
    	# initialize item varible in the AmzcockpitItem items container
        item = AmzcockpitItem()
        # natural link counter
        seo = 0
        # sponsored product counter
        ppc = 0        
        rank_offset = response.meta.get('rank_offset', 0)
        all_finds = response.css('div.s-result-item')
        for index,result in enumerate(all_finds):
            link = result.css('a.a-link-normal::attr(href)').extract_first()
            asin_ = result.css('::attr(data-asin)').extract_first()
            if not asin_:
                continue
            print(asin_,self.asin,asin_ == self.asin)
            if link is not None:
                if link.startswith('/gp/slredirect'):
                    self.sponsored = True
                    ppc = ppc + 1 + rank_offset
                    KeywordSearchSpider.ppc_overall = KeywordSearchSpider.ppc_overall + 1 + rank_offset
                    if asin_==self.asin:
                        self.found = True
                        item["keyword"] = self.keyword
                        item["product_asin"] = asin_
                        item["inpage_rank"] = ppc
                        item["overall_rank"] = KeywordSearchSpider.ppc_overall
                        item["page_number"] = KeywordSearchSpider.page_number
                        item["sponsored"] = "Yes"
                        yield item

                    else:
                        continue
            else:
            	continue

            if link is None or not link.startswith('/gp/slredirect'):
                self.sponsored = False
                seo = seo + 1 + rank_offset
                KeywordSearchSpider.seo_overall = KeywordSearchSpider.seo_overall + 1 + rank_offset
                if asin_==self.asin:
                    self.found = True
                    item["keyword"] = self.keyword
                    item["product_asin"] = asin_
                    item["inpage_rank"] = seo
                    item["overall_rank"] = KeywordSearchSpider.seo_overall
                    item["page_number"] = KeywordSearchSpider.page_number
                    item["sponsored"] = "No"
                    yield item
                else:
                    continue
            else:
            	continue
        # Set the next page
        KeywordSearchSpider.page_number = KeywordSearchSpider.page_number + 1
        next_page = "https://www.amazon.co.uk/s?k={}&page={}&qid=1599413895&ref=sr_pg_{}"\
        .format(self.keyword,KeywordSearchSpider.page_number,KeywordSearchSpider.page_number)
        # Search the first 60 pages provided the item has not been found.
        # Stop making requests to the website once the item is found.
        if KeywordSearchSpider.page_number<60 and self.found == False:
            print(100*"#")
            print(KeywordSearchSpider.page_number)
            print(100*"#")
            yield response.follow(next_page,callback=self.parse)



# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib.parse import quote_plus, urljoin
from ..items import KeywordItem


class KeywordSearchSpider(scrapy.Spider):
    name = 'keyword'
    allowed_domains = ['amazon.co.uk']
    page_number = 1
    query = "https://www.amazon.co.uk/s?k={}&ref=nb_sb_noss"
    seo = 0
    ppc = 0
    def __init__(self,keyword,asin,**kwargs):
        super().__init__(**kwargs)
        self.keyword = keyword
        self.asin = asin
        self.search_url = self.query.format(self.keyword)
        self.sponsored = False
        self.market_place = "https://www.amazon.co.uk/"
        print(100*"#")
        print(self.search_url)
        print(100*"#")
    def start_requests(self):
        yield Request(self.market_place, callback=self.parse_index)

    def parse_index(self, response):
        yield Request(self.search_url)

    def parse(self, response):
        item = KeywordItem()
        # natural link counter
        seo = 0
        # sponsored product counter
        ppc = 0        
        rank_offset = response.meta.get('rank_offset', 0)
        all_finds = response.css('div.s-result-item, .s-asin')
        for index,result in enumerate(all_finds):
            link = result.css('a.a-link-normal::attr(href)').extract_first()
            asin_ = result.css('::attr(data-asin)').extract_first()
            if not asin_:
                continue
            print(asin_,type(asin_))
            item["product_ASIN"] = asin_
            # print(rank,asin_,asin_==self.asin)
            # print(rank,asin_,self.asin, asin_==self.asin)
            if link is not None:
                if link.startswith('/gp/slredirect'):
                    self.sponsored = True
                    ppc = ppc + 1 + rank_offset
                    KeywordSearchSpider.ppc = KeywordSearchSpider.seo + ppc
                    # print(asin_,self.asin,"Sponsored",ppc)
                    if asin_==self.asin:
                        pass
                        # print(asin_,self.asin,"Sponsored","Rank",ppc)
                    else:
                        pass
                        # print(asin_,self.asin,"Sponsored",ppc)
                        # print(KeywordSearchSpider.ppc)

            if link is None or not link.startswith('/gp/slredirect'):
                self.sponsored = False
                seo = seo + 1 + rank_offset
                KeywordSearchSpider.seo = KeywordSearchSpider.seo + seo
                #print(asin_,self.asin," Not Sponsored",seo)
                if asin_==self.asin:
                    # print(asin_,self.asin," Not Sponsored","Rank",seo)
                    pass
                else:
                    # print(asin_,self.asin," Not Sponsored",seo)
                    # print(KeywordSearchSpider.seo)
                    pass

            yield item

            # if asin_==self.asin:
            #     print("Page:", KeywordSearchSpider.page_number,"Rank",rank+1)
            #     # open_in_browser(response)
            #     # import ipdb; ipdb.set_trace()
            #     # item = {}
            #     # item['asin'] = asin
            #     # print("ASIN",asin_,self.asin)
            #     # print("Rak",rank+rank_offset)
            #     # item['ranking'] = rank + rank_offset
            #     if link.startswith('/gp/slredirect'):
            #         print("Sponsored")
                #     if not self.sponsored:
                #         item['sponsored'] = True
                #         self.sponsored = True
                #     else:
                #         continue
                # else:
                #     item['sponsored'] = False
                # item['amazon_choice'] = False

                # badge = result.css('a.a-badge::attr(id)').extract_first()
                # if badge:
                #     if 'AMAZONS_CHOICE' in badge.upper():
                #         item['amazon_choice'] = True
            
            # print(result.css("h2 a").css("::attr(href)").extract())
        #print(response.css("::text"))
        

        KeywordSearchSpider.page_number = KeywordSearchSpider.page_number + 1
        next_page = "https://www.amazon.co.uk/s?k=Hair+dryer+holder&page={}&qid=1599413895&ref=sr_pg_{}"\
        .format(KeywordSearchSpider.page_number,KeywordSearchSpider.page_number)
    #   next_page = "https://www.amazon.com/Laptops-Computers-Tablets/s?rh=n%3A565108&page={}"\
    # .format(KeywordSearchSpider.page_number)

        if KeywordSearchSpider.page_number<9:
            print(100*"#")
            print(KeywordSearchSpider.page_number)
            print(100*"#")
            yield response.follow(next_page,callback=self.parse)


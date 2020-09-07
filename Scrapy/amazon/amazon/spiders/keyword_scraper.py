# -*- coding: utf-8 -*-
from urllib.parse import quote_plus, urljoin

import scrapy
from scrapy import Request


class KeywordScraperSpider(scrapy.Spider):
    name = 'keyword_scraper'
    crawlera_apikey = '7cc838061c4a47a0b479d115a856222b'
    allowed_domains = ['amazon.com']#, 'amazon.fr', 'amazon.com.br', 'amazon.ca', 'amazon.cn', 'amazon.de', 'amazon.in',
    #                    'amazon.it', 'amazon.co.jp', 'amazon.com.mx', 'amazon.nl', 'amazon.co.uk', 'amazon.es']
    search_query = '/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords={}'
    sponsored = False

    def __init__(self, keyword, asin, **kwargs):
        super().__init__(**kwargs)
        self.marketplace = "http://amazon.com/"
        self.keyword = keyword
        self.search_url = urljoin(self.marketplace, self.search_query.format(quote_plus(keyword)))
        self.asin = asin
    def start_requests(self):
        yield Request(self.marketplace, callback=self.parse_index)

    def parse_index(self, response):
        yield Request(self.search_url)

    def parse(self, response):

        rank_offset = response.meta.get('rank_offset', 0)
        print(rank_offset)
        for rank, result in enumerate(response.css('div.s-result-item'), 1):
            link = result.css('a.a-link-normal::attr(href)').extract_first()
            asin = result.css('::attr(data-asin)').extract_first()
            print(asin)
            if asin == self.asin:
                # open_in_browser(response)
                # import ipdb; ipdb.set_trace()
                item = {}
                item['asin'] = asin
                item['ranking'] = rank + rank_offset
                if link.startswith('/gp/slredirect'):
                    if not self.sponsored:
                        item['sponsored'] = True
                        self.sponsored = True
                    else:
                        continue
                else:
                    item['sponsored'] = False
                item['amazon_choice'] = False

                badge = result.css('a.a-badge::attr(id)').extract_first()
                if badge:
                    if 'AMAZONS_CHOICE' in badge.upper():
                        item['amazon_choice'] = True
                yield item

        next_page = response.css('.a-pagination .a-last a::attr(href)').extract_first()
        if next_page:
            length = len(response.css('div.s-result-item'))
            print(length)
            yield Request(response.urljoin(next_page), meta={'rank_offset': length + rank_offset})
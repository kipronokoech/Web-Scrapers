import scrapy
import re
from ..items import ReviewsItem
import json

class ReviewsScraperSpider(scrapy.Spider):
    name = 'reviews_scraper'
    allowed_domains = ['trustpilot.com']
    page = 1
    sno = 1
    start_urls = ['https://www.trustpilot.com/review/www.worldremit.com']
    # with open("../../links.txt") as infile:
    #     start_urls = [i.strip("\n") for i in infile.readlines()]
    #     start_urls = start_urls[1:]
    def __init__(self,name2=start_urls[0].split("/")[-1].split(".")[0]):
        self.name2 = name2

    @staticmethod
    def ExtractDate2(value):
        if "hour" in value or "minute" in value or "second" in value:
            return datetime.today()
        elif "day" in value:
            d = datetime.today() - timedelta(days=1)
            return d
        elif "days" in value:
            d = datetime.today() - timedelta(days=int(re.findall("\d+",value)[0]))
            return d      
        else:
            date_month = {  "Jan":1 , 
                            "Feb":2, 
                            "Mar":3, 
                            "Apr":4, 
                            "May":5, 
                            "Jun":6,
                            "Jul":7, 
                            "Aug":8, 
                            "Sep":9, 
                            "Oct":10, 
                            "Nov":11, 
                            "Dec":12
                        }
            month, day, year = value.replace(",","").split(" ")
            date_day = datetime(int(year), date_month[month], int(day))
            return date_day
    def parse(self, response):
        item = ReviewsItem()
        platform = response.css(".header-section").css("span::text").extract_first()
        item["platform"] = platform.strip("\n").strip(" ").strip("\n")
        reviews_block = response.css(".review-list")
        reviews_list = reviews_block.css(".review-card  ")
        for review in reviews_list:
            item["SNo"] = ReviewsScraperSpider.sno
            customer_info = review.css(".review__consumer-information")
            stars_string = review.css(".star-rating, .star-rating--medium")\
        	.css("img").css("::attr(alt)").extract_first()
            stars = int(re.findall("\d+",stars_string)[0])
            item["stars"] = stars
            review_date = json.loads(review.css(".review-content-header__dates").css("::text")[1].extract().strip("\n"))
            item["review_date"] = review_date["publishedDate"].split("T")[0]
            review_title = review.css(".review-content__body").css("a::text").extract_first()
            item["review_title"] = review_title.strip()
            try:
                review_text = review.css(".review-content__body").css(".review-content__text::text").extract_first()
                item["review_body"] = review_text.strip("\n").strip(" ").strip("\n").strip("\n")
            except:
                item["review_body"] = None
            item["ID"] = review.css("article, .review").css("::attr(id)").extract_first()
            try:
                item["CompanyReply"] = " ".join([i.strip() for i in review.css(".brand-company-reply__content::text").extract()])
                reply_date = review.css(".brand-company-reply__date").css("script").extract_first()
                reply_date2 = re.findall('\"publishedDate\":\"(\S+?)\"',reply_date)[0]
                item["CompanyReplyDate"], reply_time = reply_date2.split("T")
                item["CompanyReplyTime"] = reply_time.split(".")[0]
            except:
                item["CompanyReply"] = None
                item["CompanyReplyDate"] = None
                item["CompanyReplyTime"] = None
            ReviewsScraperSpider.sno = ReviewsScraperSpider.sno + 1
            yield item

        next_page = response.css(".button .button--primary, .next-page").css("a::attr(href)").extract()
        # next_page = "https://www.trustpilot.com/review/www.worldremit.com?page=2"
        if next_page:
            yield response.follow(next_page[0],callback=self.parse)




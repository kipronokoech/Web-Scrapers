from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from reviews.reviews.spiders.reviews_scraper import ReviewsScraperSpider
from scrapy.signalmanager import dispatcher

results = []
def crawler_results(signal, sender, item, response, spider):
        results.append(item)

dispatcher.connect(crawler_results, signal=signals.item_passed)
process = CrawlerProcess(get_project_settings())
process.crawl(ReviewsScraperSpider)
process.start()
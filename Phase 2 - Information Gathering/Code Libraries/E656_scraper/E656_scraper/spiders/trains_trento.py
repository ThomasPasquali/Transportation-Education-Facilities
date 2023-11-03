import scrapy


class TrainsSpider(scrapy.Spider):
    name = "Trains"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass

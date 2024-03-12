import scrapy
from gScholar.items import GscholarItem

class GooglespiderSpider(scrapy.Spider):
    name = "googlespider"
    with open('/Users/wwu/Documents/davyGoo/gScholar/gScholar/spiders/bookTest.csv') as file:
        start_urls = ['https://'+line.strip() for line in file]

    def parse(self, response):
        next_page = response.css("a[href*='https://doi.org/']")
        if (response.request.url[:26]=='https://scholar.google.com/'):
            next_page_url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q='+(next_page[16:])
            yield response.follow(next_page_url, callback = self.parse)
        cites = response.css("a[href*='/scholar?cites=']")
        item = GscholarItem()
        item["doi"] = (response.request.url)[56:]
        if len(cites)==0:
            item["cites"] = 0
        else:
            item["cites"] = cites[0].css('a::text').get()[9:]
        item["results"] = len(cites)
        yield item
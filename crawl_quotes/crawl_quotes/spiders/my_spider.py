import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.goodreads.com/quotes',
            'https://www.goodreads.com/quotes?page=2',
            'https://www.goodreads.com/quotes?page=3',
            'https://www.goodreads.com/quotes?page=4',
            'https://www.goodreads.com/quotes?page=5',
            'https://www.goodreads.com/quotes?page=6',
            'https://www.goodreads.com/quotes?page=7',
            'https://www.goodreads.com/quotes?page=8',
            'https://www.goodreads.com/quotes?page=9',
            'https://www.goodreads.com/quotes?page=10',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('.quoteText'):
            author = quote.css('a::text').extract_first()
            quote = quote.css('::text').extract()[0]
            if len(quote) <= 600:
                yield {'quote': quote, 'author': author}
import scrapy


class BooksBasicSpider(scrapy.Spider):
    name = 'books_basic'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']

    def parse(self, response):
        books = response.xpath('//h3')
        # books = response.css('h3')
        cut_tag = "../"
        for book in books:
            yield {
                'Title': book.xpath('.//a/@title').get(),
                'URL': "https://books.toscrape.com/catalogue/" + str(book.xpath('.//a/@href').get()).replace(cut_tag, "")
                # 'Title': book.css('a::attr(title)').get(),
                # 'URL': book.css('a::attr(href)').get()
            }

        # リンクをたどる（ページング）
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

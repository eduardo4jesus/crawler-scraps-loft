# -*- coding: utf-8 -*-
import scrapy


class ComedySpider(scrapy.Spider):
    name = 'blog'
    allowed_domains = ['scrapsfromtheloft.com']
    start_urls = ['https://scrapsfromtheloft.com/blog/']

    def parse(self, response):
        scraps = response.css('article').css('h2 > a::attr(href)').extract()
        for scrap_url in scraps:
            yield scrapy.Request(url=scrap_url, callback=self.parse_scrap)

    def parse_scrap(self, response):
        article = response.css('article')
        title = article.css('div > h1::text').extract_first()
        meta = response.css('div.fusion-meta-info-wrapper')
        date_str = meta.css('span')[3].css('::text').extract_first()
        categories = meta.xpath('a//text()').extract()
        tags = meta.css('span.meta-tags > a::text').extract()
        transcript = article.css('div.post-content > p *::text').extract()
        url = response.request.url

        item = {
            'title': title,
            'date_str': date_str,
            'categories': categories,
            'tags': tags,
            'transcript': transcript,
            'url': url
        }

        yield item

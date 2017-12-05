"""Change start_urls to desired typepad blog archive url
Also change condition for outgoing links to the original non-archive link"""

import scrapy
from scrapy.selector import Selector
import re

class test_spider(scrapy.Spider):
    name = "scraper"
    start_urls = ['http://ashleymorris.typepad.com/ashley_morris_the_blog/archives.html']
    custom_settings = {
        'RETRY_TIMES': 100,
    }

    
    def parse (self, response):
        for href in response.xpath('//div[@class="archive-date-based archive"]/div/ul/li/a/@href'):
            if href.extract() !="":
                full_url = response.urljoin(href.extract())
                yield scrapy.Request(full_url, callback=self.parse_link)
                
                
    def parse_link(self, response):
        for href in response.xpath('//span[@class="pager-right"]/a/@href'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_link)
        for postlink in response.xpath('//h3[@class="entry-header"]/a/@href'):
            full_url = response.urljoin(postlink.extract())
            yield scrapy.Request(full_url, callback=self.parse_post)

            
    def parse_post(self, response):
        try:
            stringdate = response.xpath('//span[@class="post-footers"]/text()').extract()[0]
        except:
            stringdate=""

        try:
            title = response.xpath('//h3[@class="entry-header"]/text()').extract()[0]
        except:
            title = ""

        try:
            author = response.xpath('//span[@class="fn"]/text()').extract()[0]
        except:
            author = ""

        try:
            body = ""
            for content in response.xpath('//div[@class="entry-body"]//text()'):
                body = body  + " " + content.extract()
        except:
            body = ""

        try:
            outgoing_links = []
            for href in response.xpath('//div[@class="entry-body"]/descendant-or-self::a/@href'):
                extracted = href.extract()
                if 'http://ashleymorris.typepad.com' not in extracted:
                    outgoing_links.append(extracted)
        except:
            outgoing_links = []

        try:
            comment_body = []
            for comment in response.xpath('//div[@class="comment-content font-entrybody"]/span'):
                try:
                    stringthing = ""
                    for text in Selector(text=comment.extract()).xpath('//span/p/text()'):
                        stringthing = stringthing + " " + text.extract()
                    comment_body.append(stringthing)
                except:
                    comment_body.append("NA")
        except:
            comment_body=[]

        try:
            comment_author= []
            for cauthor in response.xpath('//div[@class="comment-avatar"]/img/@alt'):
                extracted = cauthor.extract()
                comment_author.append(extracted)
        except:
            comment_author=[]
            
        try:
            comment_author_profile = []
            for author_link in response.xpath('//p[@class="comment-footer font-entryfooter"]'):
                extracted = Selector(text=author_link.extract()).xpath('//p/a/@href').extract()[0]
                if 'http://ashleymorris.typepad.com/ashley_morris_the_blog/' not in extracted:
                    comment_author_profile.append(extracted)
                else:
                    comment_author_profile.append("NA")
        except:
            comment_author_profile=[]

        try:
            comment_date= []
            for date in response.xpath('//p[@class="comment-footer font-entryfooter"]/a'):
                extracted = date.extract()
                if 'http://ashleymorris.typepad.com/ashley_morris_the_blog/' in extracted:
                    refined = Selector(text=extracted).xpath('//a/text()').extract()
                    comment_date.append(refined)
        except:
            comment_date=[]


        yield{
            'link': response.url,
            'date': stringdate,
            'body': body,
            'title': title,
            'outgoing_links': outgoing_links,
            'comment_body': comment_body,
            'comment_author': comment_author,
            'comment_author_profile': comment_author_profile,
            'comment_date': comment_date
        }

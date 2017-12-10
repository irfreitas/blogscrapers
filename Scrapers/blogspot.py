"""Change start_urls to desired blogspot blog
Also change condition for outgoing links """

import scrapy
from scrapy.selector import Selector
from urllib.request import urlopen
from bs4 import BeautifulSoup

class test_spider(scrapy.Spider):
    name = "scraper"
    start_urls = ['http://autismschmatism.blogspot.com/']
    custom_settings = {
        'RETRY_TIMES': 100,
    }
    
    def parse (self, response):
        page = urlopen(response.url)
        while 3 != 0:
            current = page
            current_soup = BeautifulSoup(current, "lxml")
            posts = current_soup.find_all('a', class_="timestamp-link")
            for post in posts:
                try:
                    post_link = post['href']
                    if "autismschmatism.blogspot.com" in post_link:
                        full_url = response.urljoin(post_link)
                        yield scrapy.Request(full_url, callback=self.parse_link)
                except:
                    pass
            try:
                nextpage = current_soup.find_all('a', class_="blog-pager-older-link")[0]['href']
                page = urlopen(nextpage)
            except:
                break

    
    def parse_link(self, response):
      try:
        stringdate = response.xpath('//h2[@class="date-header"]/span/text()').extract()[0]
      except:
        stringdate = ""
      
      try:
        title = response.xpath('//h3[@class="post-title entry-title"]/text()').extract()[0]
      except:
        title = ""
        
      try:
        author = response.xpath('//span[@class="fn"]/a/span/text()').extract()[0]
      except:
        author = ""
          
      try:
        body = ""
        for content in response.xpath('//div[@class="post-body entry-content"]/descendant-or-self::node()/text()'):
          body = body + " " + content.extract() # extra space necessary for some blogspot themes
      except:
        body = ""
      
      try:
        outgoing_links = []
        for href in response.xpath('//div[@class="post-body entry-content"]/descendant-or-self::a/@href'):
          extracted = href.extract()
          if 'http://autismschmatism.blogspot.com' not in extracted:
            outgoing_links.append(extracted)
      except:
        outgoing_links=[]
              try:
            post_labels = []
            for label in response.xpath('//span[@class="post-labels"]/a/text()'):
                extracted = label.extract()
                post_labels.append(extracted)
        except:
            post_labels = []

        try:
            comment_body = []
            for comment in response.xpath('//dd[@class="comment-body"]/p'):
                try:
                    stringthing = ""
                    for text in Selector(text=comment.extract()).xpath('//p/text()'):
                        stringthing = stringthing  + " " + text.extract()
                    comment_body.append(stringthing)    
                except:
                    comment_body.append("NA")
        except:
            comment_body = []

        try:
            comment_author = []
            for cauthor in response.xpath('//dt[contains(@class, "comment-author")]'):
                try:
                    if len(Selector(text=cauthor.extract().xpath('//dt[contains[@class, "comment-author")]/a/text()') !=0:
                        extracted = cauthor.extract()
                        comment_author.append(extracted)
                    else:
                        comment_author.append("NA")
        except:
            comment_author = []

        try:
            comment_author_profile = []
            for author_link in response.xpath('//dt[contains(@class, "comment-author")]'):
                if len(Selector(text=author_link.extract()).xpath('//dt[contains(@class, "comment-author")]/a/@href').extract()) != 0:
                    for link in Selector(text=author_link.extract()).xpath('//dt[contains(@class, "comment-author")]/a/@href'):
                        extracted = link.extract()
                        comment_author_profile.append(extracted)
                else:
                    comment_author_profile.append("NA")
        except:
            comment_author_profile = []

        try:
            comment_date = []
            for date in response.xpath('//dt[@class="comment-footer"]/span[@class="comment-timestamp"]/a/text()'):
                extracted = date.extract()
                comment_date.append(extracted)
        except:
            comment_date = []

      yield{
      'link': response.url,
      'date': stringdate,
      'body': body,
      'title': title,
      'outgoing_links': outgoing_links
      }

import scrapy
from allscrapy.items import AllscrapyItem
import datetime
import json

class NynewsSpider(scrapy.Spider):
    
    
    name = "new_qq_total2"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = ["https://pacaio.match.qq.com/irs/rcd?cid=52&token=8f6b50e1667f130c10f981309e1d8200&ext=7,5503,5532,5533,8101,8102&page=1&isForce=1&expIds=20201125A04EE3|20201120A04SWH|20201125A063A3|20201125A067P0|20201125A05K9Z|20201125A05FS3&callback=__jp5"]
                    
    def parse(self, response):
        # yield scrapy.Request(f"{self.start_urls[0]}", callback=self.parse_article_urls) 
        page_type_list = [
                            '55,7,5502,5505,5506,5530',\
                            '7,5503,5532,5533,8101,8102',\
                            '7,5507,550,5509,551,5529,550,5520,552,5522,5523',\
                            '7603,7606,7608,7609,7613,215,216,5501',\
                            '614,603,605,611,612,613,615,620,618',\
                            '604,609',\
                            '602,608,622',\
                            '619,617,610',\
                            '4101,4104,604',\
                            '4102',\
                            '4109,4110',\
                            '608',\
                            '1022,1007,1009,1010,1011,1013,1014,1015,1016,1017,1018,1019,1020',\
                            '1004,1017,1018,1019,1020,1024,1021,1023',\
                            '1002,1003',
                            ]
        page = 1
        while page < 20:
            next_urls = f'https://pacaio.match.qq.com/irs/rcd?cid=52&token=8f6b50e1667f130c10f981309e1d8200&ext=7,5503,5532,5533,8101,8102&page={page}&isForce=1&expIds=20201125A04EE3|20201120A04SWH|20201125A063A3|20201125A067P0|20201125A05K9Z|20201125A05FS3&callback=__jp5'
            yield scrapy.Request(f"{next_urls}", callback=self.parse_article_urls) 
            page += 1
            
    def parse_article_urls(self, response):
        
        response_json = json.loads(response.text[6:-1])
        for data_inform in response_json['data']:
            article_urls = data_inform['vurl']
            category = data_inform['category_chn']
            yield scrapy.Request(f"{article_urls}", callback=self.parse_content, meta={'category':category}) 
            
    def parse_content(self, response):
        
        category = response.meta['category']
        title = response.xpath('//div[@class="LEFT"]/h1/text()').get()
        img = response.xpath('//div[@class="content-article"]/p/img/@src').getall()
    
        contents_xpath = response.xpath('//div[@class="content-article"]/p')
        contents = []
        for content_xpath in contents_xpath:
            content = content_xpath.xpath('.//text()|./img/@src').getall()
            contents.append(content[0])
        contents = self.content_filter(contents)

        if len(contents) >0:    
            print(f'=============={category}-{title}==={response.url}======================\n {contents}')

            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            item = AllscrapyItem()
            item["url"] = response.url
            item["time"] = f"{datetime.date.today()}_{current_time}"
            item["title"] = title
            item["category"] = category
            item["content"] = contents
            item['time_decline'] = datetime.datetime.utcnow()
            yield item
        
    def content_filter(self, contents):
        
        _contents = []
        for content in contents:
            
            content = content.strip()
            if '本文作者原创' in content:
                continue
            if content != '':
                _contents.append(content)
        return _contents
    
    

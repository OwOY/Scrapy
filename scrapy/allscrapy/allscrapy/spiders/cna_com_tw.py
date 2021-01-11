import scrapy
from allscrapy.items import AllscrapyItem
import datetime
import json

class NynewsSpider(scrapy.Spider):
    
    name = "www_cna_com"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = ["https://www.cna.com.tw/list/aie.aspx"]

    def parse(self, response):
        
        category_list = response.xpath("//ul[@class='main-menu']/li/a/text()").getall()[2:-3]
        category_url_list = response.xpath("//ul[@class='main-menu']/li/a/@href").getall()[2:-3]
        i = 0
        category_api_id = category_url_list[i].split('/')[-1].replace('.aspx','')
        formdata = {"action":"0","category":f"{category_api_id}","pagesize":"20","pageidx":2}
        request_body = json.dumps(formdata).encode('utf-8')
        print(category_list[i], category_api_id, request_body)
        yield scrapy.FormRequest('https://www.cna.com.tw/cna2018api/api/WNewsList',\
                                body = request_body,\
                                callback=self.parse_article_urls,\
                                meta = {'category':category_list[i]})
        # while True:
        #     try:
        #         category_api_id = category_url_list[i].split('/')[-1].replace('.aspx','')
        #         formdata = {"action":"0","category":f"{category_api_id}","pagesize":"20","pageidx":2}
        #         request_body = json.dumps(formdata)
        #         print(category_list[i], category_api_id, request_body)
        #         yield scrapy.FormRequest('https://www.cna.com.tw/cna2018api/api/WNewsList',\
        #                                 formdata = request_body,\
        #                                 callback=self.parse_article_urls,\
        #                                 meta = {'category':category_list[i]})
        #     except:
        #         print('231')
        #         break
        #     i += 1

    def parse_article_urls(self, response):

        # print(response.meta['category'])
        print(response.text)
        print(response.json())


        
        

    # def parse_content(self, response):
        
    #     title = response.meta['title']
    #     contents = response.xpath('//div[@class="text boxTitle boxText"]/p/descendant::text()|//div[@class="text boxTitle boxText"]/div[@class="photo boxTitle"]/a/@href').getall()
    #     contents = self.content_filter(contents)
    #     print(f'=================={title}==================\n{response.url}\n{contents}')
    #     now = datetime.datetime.now()
    #     current_time = now.strftime("%H:%M:%S")
        
    #     item = AllscrapyItem()
    #     item["url"] = response.url
    #     item["time"] = f"{datetime.date.today()}_{current_time}"
    #     item["title"] = title
    #     item["category"] = response.meta['category']
    #     item["content"] = contents
    #     item['time_decline'] = datetime.datetime.utcnow()
    #     yield item
        
    # def content_filter(self, contents):
        
    #     _contents = []
    #     for content in contents:
            
    #         content = content.strip()
    #         try:
    #             content = content.split('報導〕')[1]
    #         except:
    #             pass
    #         if '不用抽 不用搶' in content:
    #             continue
    #         if '請繼續往下閱讀...' in content:
    #             continue
    #         if '點我下載APP' in content:
    #             break
            
    #         if content != '':
    #             _contents.append(content)

    #     return _contents
    
    

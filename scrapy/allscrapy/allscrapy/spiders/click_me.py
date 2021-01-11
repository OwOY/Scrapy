import scrapy
from allscrapy.items import AllscrapyItem
import datetime
from scrapy import FormRequest

class NynewsSpider(scrapy.Spider):
    
    name = "clickme_net"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = ["https://clickme.net/c/kuso"]
    
    def parse(self, response):
        
        categorys = response.xpath("//li[@class='menu-item ']/a/span/text()").getall()
        category_urls = response.xpath("//li[@class='menu-item ']/a/@href").getall()
        i = 2
        while i < len(categorys):
            if i != 4:
                category_url = category_urls[i].replace('/c/','')
                for page in range(1,20):
                    yield FormRequest(f'https://api.clickme.net/article/list?key=clickme',\
                                        formdata={'articleType':'article',\
                                        'subtype':'category',\
                                        'subtypeSlug':category_url,\
                                        'limit':'18',\
                                        'page':f'{page}'},\
                                        callback=self.parse_article_urls, meta={"category" : categorys[i]})
            i += 1
    
    def parse_article_urls(self, response):
        
        datas = response.json()
        try:
            for data in datas['data']['items']:
                yield scrapy.Request(f"{data['url']}", callback=self.parse_article_contents, meta={"category" : response.meta['category']})
        except:
            pass    
        
    def parse_article_contents(self, response):
        
        title = response.xpath("//div[@class='article-banner-title']/h1/text()").get().strip()
        imgs = response.xpath("//article[@class='article-detail-content article-left']//img/@src").getall()
        
        if response.xpath("//article[@class='article-detail-content article-left']//text()") != []:
            contents = response.xpath("//article[@class='article-detail-content article-left']//text()|//article[@class='article-detail-content article-left']//img/@src").getall()
        else:
            contents = response.xpath("//article[@class='article-detail-content article-center']//text()|//article[@class='article-detail-content article-center']//img/@src").getall()
            imgs = response.xpath("//article[@class='article-detail-content article-center']//img/@src").getall()
        contents = self.content_filter(contents, imgs)
        print(f'=================={title}==================\n{response.url}')
        for content in contents:
            print(content)
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        item = AllscrapyItem()
        item["url"] = response.url
        item["time"] = f"{datetime.date.today()}_{current_time}"
        item["title"] = title
        item["category"] = response.meta['category']
        item["content"] = contents
        # item['time_decline'] = datetime.datetime.utcnow()
        yield item

    def content_filter(self, contents, imgs):
        
        _contents = []
        content_word = ''
        for content in contents:
            content = content.strip().replace(u'\u3000','').replace('魯拉拉','')
            if content in imgs:
                if content_word != '':
                    _contents.append(content_word)
                content_word = ''
                if 'http' not in content:
                    content = f'http:{content}'
                    _contents.append(content)
            else:
                if '傳送門' in content:
                    continue
                if '延伸閱讀' in content:
                    continue
                if '按此前往成人站' in content:
                    break
                if content == '、':
                    continue
                
                content_word += content
        
        if len(content_word) > 1:
            _contents.append(content_word)
            
        return _contents

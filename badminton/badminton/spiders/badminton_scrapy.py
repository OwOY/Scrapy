# -*- coding: utf-8 -*-
import scrapy
import requests
from badminton.items import BadmintonItem

class BadmintonScrapySpider(scrapy.Spider):
    name = 'badminton_scrapy'
    allowed_domains = ['www.badmintontw.com']
    start_urls = ['https://www.badmintontw.com/taipei.php?date=7/14']

    def parse(self, response):
        # -------------------------------------------------------------------------------
        Team = response.xpath('//td[@class="name"]')
        Team = [T.xpath('.//text()') for T in Team]
        # Team =  [T[0] if T != [] else '??' for T in Team]
        # -------------------------------------------------------------------------------
        Country = response.xpath('//td[2]')
        Country = [C.xpath('.//text()') for C in Country]
        # Country = [C[0] if C != [] else '??' for C in Country]
        # -------------------------------------------------------------------------------
        Time = response.xpath('//td[3]')
        Time = [T.xpath('.//text()') for T in Time]
        # Time = [T[0] if T != [] else '??' for T in Time]
        # -------------------------------------------------------------------------------
        Location = response.xpath('//td[4]')
        Location = [L.xpath('.//text()') for L in Location]
        # Location = [L[0] if L != [] else '??' for L in Location]
        # -------------------------------------------------------------------------------
        Lv = response.xpath('//td[5]')
        Lv = [L.xpath('.//text()') for L in Lv]
        # Lv = [L[0] if L != [] else '??' for L in Lv]
        # -------------------------------------------------------------------------------
        Fee = response.xpath('//td[6]')
        Fee = [F.xpath('.//text()') for F in Fee]
        # Fee = [F[0] if F != [] else '??' for F in Fee]
        # -------------------------------------------------------------------------------
        Court = response.xpath('//td[7]')
        Court = [C.xpath('.//text()') for C in Court]
        # Court = [C[0] if C != [] else '??' for C in Court]
        # -------------------------------------------------------------------------------
        Ball = response.xpath('//td[8]')
        Ball = [B.xpath('.//text()') for B in Ball]
        # Ball = [B[0] if B != [] else '??' for B in Ball]
        # -------------------------------------------------------------------------------

        for a,b,c,d,e,f,g,h in zip(Team,Country,Time,Location,Lv,Fee,Court,Ball):
            item = BadmintonItem()            
            item['Team'] = a.get()
            item['Country'] = b.get()
            item['Time'] = c.get()
            item['Location'] = d.get()
            item['Lv'] = e.get()
            item['Fee'] = f.get()
            item['Court'] = g.get()
            item['Ball'] = h.get()
            yield item
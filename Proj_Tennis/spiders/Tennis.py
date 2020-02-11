from scrapy import Spider
from scrapy import Request
from Proj_Tennis.items import ProjTennisItem
import re

class ProjTennisSpider(Spider):
    name = 'Tennis'
    allowed_urls = ['https://www.atptour.com/']
    start_urls = ['https://www.atptour.com/en/rankings/singles?rankDate=2020-02-03&rankRange=1-5000']
    def parse(self, response):
        result_urls = response.xpath('//tbody/tr/td[4]/a/@href').extract()
        result_urls = ['https://www.atptour.com' + i for i in result_urls]

        for url in result_urls:
            yield Request(url=url, callback=self.parse_review)

    def parse_review(self, response):
        
        # pull review data
        f_name = response.xpath('//div[@class="first-name"]/text()').extract_first().strip()
        l_name = response.xpath('//div[@class="last-name"]/text()').extract_first().strip()
        age = response.xpath('//tr[1]/td[1]/div/div[@class="table-big-value"]/text()').extract_first().strip()
        yr_pro = response.xpath('//tr[1]/td[2]/div/div[@class="table-big-value"]/text()').extract_first().strip()
        wt = response.xpath('//tr[1]/td[3]/div/div[@class="table-big-value"]/span/text()').extract_first()
        #re.sub("[kg()]",'',response.xpath('//tr[1]/td[3]/div/div[@class="table-big-value"]/span/text()').extract_first())
        ht = response.xpath('//tr[1]/td[4]/div/div[@class="table-big-value"]/span/text()').extract_first()
        #re.sub("[cm()]",'',response.xpath('//tr[1]/td[4]/div/div[@class="table-big-value"]/span/text()').extract_first())
        if response.xpath('//tr[2]/td[1]/div/div[@class="table-value"]/text()').extract_first().find(',')==-1:#ck if no country (based on no comma in entry)
            birthplace = ''
        else:
            birthplace = response.xpath('//tr[2]/td[1]/div/div[@class="table-value"]/text()').extract_first().rsplit(',', 1)[1].strip() 
        rank_2020 = response.xpath('//tr[1]/td[2]/div[1]/text()').extract()[3].strip()
        rank_career = response.xpath('//tr[2]/td[2]/div[1]/text()').extract()[3].strip()
        win_career = response.xpath('//tr[2]/td[3]/div[1]/text()').extract()[3].split('-')[0].split()
        loss_career = response.xpath('//tr[2]/td[3]/div[1]/text()').extract()[3].split('-')[1].split()
        titles_career = response.xpath('//tr[2]/td[4]/div[1]/text()').extract()[3].strip()
        prize_career = float(re.sub(r'[^\d.]', '',response.xpath('//tr[2]/td[5]/div[1]/text()').extract_first().strip()))

        # create review item
        item = ProjTennisItem()
        item['f_name'] = f_name
        item['l_name'] = l_name
        item['age'] = age
        item['yr_pro'] = yr_pro
        item['wt'] = wt
        item['ht'] = ht
        item['birthplace'] = birthplace
        item['rank_2020'] = rank_2020
        item['rank_career'] = rank_career
        item['win_career'] = win_career
        item['loss_career'] = loss_career
        item['titles_career'] = titles_career
        item['prize_career'] = prize_career
        yield item



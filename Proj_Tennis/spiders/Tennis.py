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
        #all overview stats
        stats_urls = ['https://www.atptour.com' + i for i in result_urls]
        #finals stats (no longer used)
        #t = map(lambda x: x.replace('overview', 'titles-and-finals'), result_urls)
        #finals_urls = ['https://www.atptour.com' + i for i in t]

        #get all overview stats
        for url in stats_urls:
            yield Request(url=url, callback=self.parse_stats)

    def parse_stats(self, response):
        
        # pull stats data
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
        rank_2020 = int(response.xpath('//tr[1]/td[2]/div[1]/@data-singles').extract_first()) #.strip()
        rank_career = int(response.xpath('//tr[2]/td[2]/div[1]/@data-singles').extract_first()) #[3].strip()
        win_career = int(response.xpath('//tr[2]/td[3]/div[1]/@data-singles').extract_first().split('-')[0])
        loss_career = int(response.xpath('//tr[2]/td[3]/div[1]/@data-singles').extract_first().split('-')[1])
        titles_career = int(response.xpath('//tr[2]/td[4]/div[1]/@data-singles').extract_first()) #[3].strip()
        prize_career = float(re.sub(r'[^\d.]', '',response.xpath('//tr[2]/td[5]/div[1]/@data-singles').extract_first()))
        if response.xpath('//tr[2]/td[3]/div/div[@class="table-value"]/text()').extract_first().strip()=='':#ck if blank
            l_hand = ''
            backhand = ''
        else:
            l_hand = response.xpath('//tr[2]/td[3]/div/div[@class="table-value"]/text()').extract_first().split(',')[0].strip() 
            backhand = response.xpath('//tr[2]/td[3]/div/div[@class="table-value"]/text()').extract_first().split(',')[1].strip() 
        
        # create item-stats
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
        item['l_hand'] = l_hand
        item['backhand'] = backhand
        #yield item
        
        #add new tab (titles and finals) to get finals data
        t = response.url.replace('overview','titles-and-finals')
        request = yield Request(t,meta={'my_meta_item':item},callback=self.parse_finals)
        
    def parse_finals(self, response):
        
        item = response.meta['my_meta_item']
        # pull finals data
        t = response.xpath('//*[@id="singlesDropdown"]/ul/li[2]/text()').extract_first().strip()
        finals_career = int(t[t.find("(")+1:t.find(")")])
        
        # create item-finals
        #item = ProjTennisItem()
        item['finals_career'] = finals_career
        yield item
        
        


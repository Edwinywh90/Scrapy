import scrapy
import json
import datetime

class StarhubSpider(scrapy.Spider):
    name = 'starhub'
    start_urls = ['https://www.starhubtvplus.com/epg/']
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB",
        "Origin" : "https://www.starhubtvplus.com",
        "Referer": "https://www.starhubtvplus.com/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "x-application-key": "5ee2ef931de1c4001b2e7fa3_5ee2ec25a0e845001c1783dc",
        "x-application-session": "01F2G66TY3GT1Z6GQP957AN6AP1E638AC633",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    
    
    def parse(self, response):
        hoursBackward = 24
        hoursForward = 24 * 2
        url = f"https://api.starhubtvplus.com/epg?operationName=webEpg&variables=%7B%22hoursBackward%22%3A{hoursBackward}%2C%22hoursForward%22%3A{hoursForward}%2C%22programsByDate%22%3Afalse%7D&query=query%20webEpg(%24hoursBackward%3A%20Int%2C%20%24hoursForward%3A%20Int)%20%7B%0A%20%20nagraEpg%20%7B%0A%20%20%20%20items%20%7B%0A%20%20%20%20%20%20channelId%3A%20tvChannel%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20image%0A%20%20%20%20%20%20isIptvMulticast%0A%20%20%20%20%20%20isOttUnicast%0A%20%20%20%20%20%20title%3A%20description%0A%20%20%20%20%20%20programs(hoursBackward%3A%20%24hoursBackward%2C%20hoursForward%3A%20%24hoursForward)%20%7B%0A%20%20%20%20%20%20%20%20channel%20%7B%0A%20%20%20%20%20%20%20%20%20%20isIptvMulticast%0A%20%20%20%20%20%20%20%20%20%20isOttUnicast%0A%20%20%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20endTime%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20startOverSupport%0A%20%20%20%20%20%20%20%20startTime%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20__typename%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20__typename%0A%20%20%7D%0A%7D%0A"
        
        yield scrapy.Request(url,
                callback=self.parse_api,
                headers=self.headers)
    

    def parse_api(self, response):
        raw_data = response.text
        data = json.loads(raw_data)

        for channel in data['data']['nagraEpg']['items']:
            channelId = channel['channelId']
            
            for program in channel['programs']:
                title = program['title']
                
                # convert unixtime to local time
                start_time = program['startTime']
                start_time = datetime.datetime.fromtimestamp(start_time/1000)    

                end_time = program['endTime']
                end_time = datetime.datetime.fromtimestamp(end_time/1000)            

                date = self.get_broadcast_date(start_time)

                yield {
                     'ChannelId' : channelId,
                     'Title' : title,
                     'Date' : f"{date:%Y-%m-%d}",
                     'StartTime' : f"{start_time:%Y-%m-%d %H:%M:%S}",
                     'EndTime' : f"{end_time:%Y-%m-%d %H:%M:%S}"
                }

    def get_broadcast_date(self, dt):
        standard_time = datetime.time(3,0)

        if dt.time() >= standard_time:
            return dt.date()
        else:
            return dt - datetime.timedelta(days=1)
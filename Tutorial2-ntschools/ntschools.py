import scrapy
import json

class NtschoolsSpider(scrapy.Spider):
    name = 'ntschools'
    start_urls = ['https://directory.ntschools.net/#/schools']
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh-TW;q=0.6,zh;q=0.5",
        "Referer": "https://directory.ntschools.net/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        #"X-Requested-With": "Fetch",
    }

    def parse(self, response):
        url = 'https://directory.ntschools.net/api/System/GetAllSchools'

        yield scrapy.Request(url,
                callback=self.parse_api, 
                headers = self.headers)

    def parse_api(self, response):
        base_url = 'https://directory.ntschools.net/api/System/GetSchool?itSchoolCode='
        raw_data = response.body
        data = json.loads(raw_data)

        for school in data:
            school_code = school['itSchoolCode']
            school_url = base_url+school_code
            request = scrapy.Request(school_url, 
                        callback=self.parse_school,
                        headers=self.headers)
            yield request

    def parse_school(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        yield {
            'Name': data['name'],
            'PhysicalAddress': data['physicalAddress']['displayAddress'],
            'PostalAddress': data['postalAddress']['displayAddress'],
            'Email': data['mail'],
            'Phone': data['telephoneNumber']
        }
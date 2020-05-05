import scrapy
import re
from io import BytesIO
from PIL import Image
import pytesseract
import scrapy_splash
import random
import logging

class YicheSpider(scrapy.Spider):

    def __init__(self):
        self.base_url = "http://i.yiche.com/authenservice/common/CheckCode.aspx?guid="

    name = "yiche"
    start_urls = ["http://i.yiche.com/u82347697/"]

    def start_requests(self):
        yield scrapy_splash.SplashRequest("http://i.yiche.com/authenservice/login.aspx",callback=self.parse_2,args={"wait":1})

    def parse_2(self,response):
        wangye_response = response.meta.get("wangye_data")
        if not wangye_response:
            self.login_data = {}
            self.login_data["txt_LoginName"] = "13256343203"
            self.login_data["txt_Password"] = "ys4Bs1JdPAc92SZLohfW3ezE8ZmQoj9QoxXx1BDkbgdKlOsHqCH7pVFxpye+hjuXOwJapX6Ch5mMHUfYBpBgQihhPQsdATSpW4JJ8M00K28qee8lqZ9lM395cD8iC3KjkzEpbP5PwquQ52QC8q3/h84TYIqXAZfABbTacVC7xcc="
           # self.img_url_half = response.xpath("//img[@id='img_code']/@src").extract_first()
            self.guid = self.generate_guid()
            img_url = self.base_url+self.guid
            yield scrapy.Request(img_url,
                    meta = {"wangye_data":response},
                    callback = self.parse_2)
        else:
            code = self.recognise_code(response.body)
            self.login_data["txt_Code"] = input()
            self.login_data["guid"] = self.guid
            self.login_data["returnurl"] = "http://i.yiche.com"
            self.login_data["cbx_keepState"] = "true"
            yield scrapy.FormRequest("http://i.yiche.com/ajax/Authenservice/login2.ashx",formdata=self.login_data,callback=self.start_it)

    def parse(self,response):
        with open("index.html","wb") as f:
            f.write(response.body)

    def recognise_code(self,data):
        with open("code.gif","wb") as f:
            f.write(data)
        img = Image.open(BytesIO(data))
        img = img.convert("L")
        code = pytesseract.image_to_string(img)
        img.close()
        logging.info(code)
        return code

    def generate_guid(self):
        guid = ''
        for i in range(6):
            guid+=random.choice("1234567890")
        guid+="-"
        for i in range(3):
            for i in range(4):
                guid+=random.choice("abcdefghijklmnopqrstuvwzyx1234567890")
            guid+="-"
        for i in range(12):
            guid+=random.choice("abcdefghijklmnopqrstuvwzyx1234567890")
        return guid

    def start_it(self,response):
        logging.info(response.headers)
        yield scrapy.Request(self.start_urls[0],callback=self.parse)


        




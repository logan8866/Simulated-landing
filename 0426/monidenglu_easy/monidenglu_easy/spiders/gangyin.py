import scrapy

class GangyinLogin(scrapy.Spider):

    name = "gangyinlogin"
    start_urls = ["http://member.banksteel.com"]
    def __init__(self):
        self.login_url = "http://login.banksteel.com/login.htm"

    #def 

    def start_requests(self):
        yield scrapy.Request(self.login_url,callback=self.parse1)

    def parse1(self,response):
        yield {"item":response.text}
        sel = response.xpath("//div[@class='login-box']//input")
        fd = dict(zip(sel.xpath("./@name").extract(),sel.xpath("./@value").extract()))
        fd["username"] = "13256343203"
        fd["password"] = "wyq123456789"
        yield scrapy.http.FormRequest(self.login_url,formdata=fd,callback=self.parse2)

    def parse2(self,response):
        yield {"item":response.text}

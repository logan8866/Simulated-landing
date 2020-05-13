from selenium import webdriver
from hashlib import md5
import requests
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
import time

class Login12306():

    def __init__(self):
        self.__plat_name = "wangyiqing8866"
        self.__plat_password = "wyq123456789"
        self.__plat_softid = "904829"
        self.__plat_pwd = md5(self.__plat_password.encode("utf8")).hexdigest()
        self.__base_headers = {
            "user":self.__plat_name,
            "pass2":self.__plat_pwd,
            "softid":self.__plat_softid,
            "codetype":9004,
        }
        self.plat_site = 'http://upload.chaojiying.net/Upload/Processing.php'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--no-sandbox")
        #self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(5)
        self.files = {"userfile":()}

    def login_it(self):
        self.driver.get("https://kyfw.12306.cn/otn/resources/login.html")
        self.driver.maximize_window()
        pwd_login_btn = self.driver.find_element_by_xpath("//li[@class='login-hd-account']/a")
        pwd_login_btn.click()
        name_model = self.driver.find_element_by_xpath("//input[@id='J-userName']")
        pwd_model = self.driver.find_element_by_xpath("//input[@id='J-password']")
        name_model.send_keys("nousername666")
        pwd_model.send_keys("nopassword666")
        button = self.driver.find_element_by_xpath("//a[@id='J-login']")
        code_img = self.driver.find_element_by_xpath("//img[@id='J-loginImg']")
        position = self.get_img_position(code_img)
        img = self.get_img(position)
        self.files["userfile"] = ("img.png",img)
        position_click = requests.post(self.plat_site,data=self.__base_headers,files=self.files)
        position_click = position_click.json()
        for i in position_click["pic_str"].split("|"):
            x_offset = i.split(",")[0]
            y_offset = i.split(",")[1]
            ActionChains(self.driver).move_to_element_with_offset(code_img,x_offset,y_offset).click().perform()
            time.sleep(0.5)
        button.click()

    def get_img_position(self,code_img):
        top = code_img.location["y"]
        bottom = code_img.location["y"]+code_img.size["height"]
        left = code_img.location["x"]
        right = code_img.location["x"]+code_img.size["width"]
        return (top,bottom,left,right)

    def get_img(self,position):
        screenshot = self.driver.get_screenshot_as_file("./vollscreen.png")
        img = Image.open('./vollscreen.png')
        code_img = img.crop((position[2],position[0],position[3],position[1]))
        code_img.save("./codeimg.png")
        img.close()
        code_img.close()
        with open("./codeimg.png","rb") as f:
            img = f.read()
        return img

login = Login12306()
login.login_it()











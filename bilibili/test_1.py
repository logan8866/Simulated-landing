from selenium import webdriver
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

def slid_track(distance):
    current = 0
    v = 0
    t = 0.2
    mid = distance*2/3
    track = []
    while current<distance:
        if current<mid:
            a = 2
        else:
            a=-1
        v0 = v
        v = v0+a*t
        s = v0*t+a*t*t/2
        current += s
        track.append(round(s))
    return track


def execute_slid(track,driver,slid_button):
    ActionChains(driver).click_and_hold(slid_button).perform()
    for i in track:
        ActionChains(driver).move_by_offset(xoffset=i,yoffset=random.uniform(1,3)).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()


def caculate_distance(less_img,voll_img):
    for i in range(less_img.size[0]):
        for j in range(voll_img.size[1]):
            if not img_equal(less_img,voll_img,i,j):
                distance = i-6
                return distance


def img_equal(less_img,voll_img,x,y):
    pixel1 = less_img.load()[x,y]
    pixel2 = voll_img.load()[x,y]
    wucha = 30
    if abs(pixel1[0]-pixel2[0])<wucha and abs(pixel1[1]-pixel2[1])<wucha:
        return True
    else:
        return False


options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
driver.get("https://passport.bilibili.com/login")
driver.maximize_window()
login_name = driver.find_element_by_xpath("//input[@id='login-username']")
login_name.send_keys("13256343203")
login_pwd = driver.find_element_by_xpath("//input[@id='login-passwd']")
login_pwd.send_keys("wyq123456789")
button = driver.find_element_by_xpath("//a[@class='btn btn-login']")
button.click()
slid_button = driver.find_element_by_xpath("//div[@class='geetest_slider_button']")
time.sleep(1)
less_canvas = driver.find_element_by_xpath("//canvas[@class='geetest_canvas_slice geetest_absolute']")
top,bottom,left,right = less_canvas.location["y"],less_canvas.location["y"]+less_canvas.size["height"],less_canvas.location["x"],less_canvas.location["x"]+less_canvas.size["width"]
#
js = "document.getElementsByClassName('geetest_canvas_slice geetest_absolute')[0].style='display:none;'"
driver.execute_script(js)
screenshot = driver.get_screenshot_as_file("./voll_screen.png")
im = Image.open("./voll_screen.png")
less_img = im.crop((left,top,right,bottom))
less_img.save("./less_img.png")
#
js = "document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute')[0].style=''"
driver.execute_script(js)
screenshot = driver.get_screenshot_as_file("./voll_screen.png")
im = Image.open("./voll_screen.png")
voll_img = im.crop((left,top,right,bottom))
voll_img.save("./voll_img.png")
#
js = "document.getElementsByClassName('geetest_canvas_slice geetest_absolute')[0].style=''"
driver.execute_script(js)
js = "document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute')[0].style='display:none;'"
driver.execute_script(js)
distance = caculate_distance(less_img,voll_img)
track = slid_track(distance)
execute_slid(track,driver,slid_button)



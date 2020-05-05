from selenium import webdriver
from PIL import Image
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
import time 
time.sleep(2)
less_canvas = driver.find_element_by_xpath("//canvas[@class='geetest_canvas_slice geetest_absolute']")
top,bottom,left,right = less_canvas.location["y"],less_canvas.location["y"]+less_canvas.size["height"],less_canvas.location["x"],less_canvas.location["x"]+less_canvas.size["width"]
screenshot = driver.get_screenshot_as_file("./voll_screen.png")
im = Image.open("./voll_screen.png")
less_img = im.crop((left,top,right,bottom))
less_img.save("./less_img.png")

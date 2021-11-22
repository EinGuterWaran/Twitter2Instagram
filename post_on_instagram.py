import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import autoit
import time
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

ig_username = os.environ.get('ig_username')
ig_pw = os.environ.get('ig_pw')
mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) "
                 "AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile "
                 "Safari/535.19"}
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=chrome_options)

driver.get('https://www.instagram.com/accounts/login/')

time.sleep(3)
driver.find_element_by_xpath("/html/body/div[4]/div/div/button[1]").click()
time.sleep(3)
driver.find_element_by_name("username").send_keys(ig_username)
driver.find_element_by_name("password").send_keys(ig_pw)
time.sleep(3)
# driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/article/div/div/div/form/div[7]/button""").click()
driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/div/form/div/div[6]/button/div").click()

time.sleep(4)
driver.get('https://www.instagram.com/' + ig_username)

dir_path = os.path.abspath(__file__)
dir_path = os.path.dirname(dir_path) + "\\tweet_images\example.jpg"

ActionChains(driver).move_to_element(driver.find_element_by_xpath(
    """//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]""")).click().perform()
handle = "[CLASS:#32770; TITLE:Öffnen]"
autoit.win_wait(handle, 3)
autoit.control_set_text(handle, "Edit1", dir_path)
autoit.control_click(handle, "Button1")

time.sleep(2)

driver.find_element_by_xpath("""//*[@id="react-root"]/section/div[1]/header/div/div[2]/button""").click()

time.sleep(2)

txt = driver.find_element_by_class_name('_472V_')
txt.send_keys('')
txt = driver.find_element_by_class_name('_472V_')
txt.send_keys('test')  # Description
txt.send_keys(Keys.ENTER)

driver.find_element_by_xpath("""//*[@id="react-root"]/section/div[1]/header/div/div[2]/button""").click()

# basic template to use selenium
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# # from selenium.webdriver.common.keys import Key
# from time import sleep

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")

# # go to google
# driver = webdriver. Chrome(chrome_options=chrome_options, executable_path="C:\Users\souha\OneDrive\Desktop\Dev\scraper")
# driver.get("https://www.reddit.com/")
# driver.maximize_window()

# global url , sub 
# sub=[]
# header = {'User-Agent': 'Mozilla/5.0'}         

# def sub_red(key):
#     search = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/header/div/div[1]/div[2]/div/form/input")
#     search.send_keys(key)
#     search.send_keys(key.ENTER)
#     sleep(4)
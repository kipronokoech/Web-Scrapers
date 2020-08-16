# import os

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys



# PATH = "/home/kiprono/chromedriver"
# url = "https://www.worldometers.info/coronavirus/"
# driver = webdriver.Chrome(PATH)
# # options = Options()
# # options.headless = True
# # driver = webdriver.Chrome(options=options)

# driver.get(url)

# # driver.close() #closes one tab
# # driver.quit() #closes the all browser

# print(driver.title)

# search = driver.find_element_by_name("form-control input-sm")

# print(search.text)



# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time


# PATH = "/home/kiprono/chromedriver"
# driver = webdriver.Chrome(PATH)
# driver.get("https://twitter.com/koech_kiprono1/following")
# # assert "Kiprono Elijah Koech" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("Facebook")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# time.sleep(10)
# # driver.close()


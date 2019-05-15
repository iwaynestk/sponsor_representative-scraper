# Initiation
from selenium import webdriver
from time import sleep
import os


# Open up a Firefox browser and navigate to web page. 
driver = webdriver.Chrome()
driver.get("http://exam.sac.net.cn/pages/registration/sac-publicity-report.html")


# Get the handle of current page
now_handle = driver.current_window_handle
print(now_handle)


# Get the list of all the links you want to click on
driver.find_element_by_xpath("""//*[@id="publicityOtherList"]/tr[1]/td[10]/a""").click()


# Get all the handles of open pages
all_handles = driver.window_handles
print(all_handles)


# Switch to the page we just opened
now_handle = all_handles[1]
driver.switch_to.window(now_handle)


# Click on the page we just opened
driver.find_element_by_xpath("""//*[@id="1"]/td[2]/a""").click()
all_handles = driver.window_handles
now_handle = all_handles[2]
driver.switch_to.window(now_handle)

# Then we do some scraping here. Now we would like to close this window and go for the next window. 
# Scraping


#Close the current window and go back to the previous window
driver.close()
all_handles = driver.window_handles
now_handle = all_handles[-1]
driver.switch_to.window(now_handle)
driver.close()




# # Close browser once task is completed
# driver.quit()








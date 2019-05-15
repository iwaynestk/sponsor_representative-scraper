# Initiation
from selenium import webdriver
from time import sleep
import os


# Open up a Firefox browser and navigate to web page. 
driver = webdriver.Chrome()
driver.get("http://exam.sac.net.cn/pages/registration/sac-publicity-report.html")


# Get the handle of current page
now_handle = driver.current_window_handle


# Get the list of all the links you want to click on
driver.find_element_by_xpath("""//*[@id="publicityOtherList"]/tr[1]/td[10]/a""").click()


# Get all the handles of open pages
all_handles = driver.window_handles


# Switch to the page we just opened
now_handle = all_handles[1]
driver.switch_to.window(now_handle)

# Now we would like to get the url of this page. 
currentUrl = driver.current_url
print(currentUrl)


# In this loop, we would open the links on this page one by one. After each iteration, we would close the window we just opened and then return to the previous window. 
for loop_num in range(1, 100): 
    # Click on the page we just opened
    driver.find_element_by_xpath("""//*[@id="%s"]/td[2]/a""" % loop_num).click()
    all_handles = driver.window_handles
    now_handle = all_handles[2]
    driver.switch_to.window(now_handle)

    # Then we do some scraping here. Now we would like to close this window and go for the next window. 
    # Scraping
    sleep(2)

    #Close the current window and go back to the previous window
    driver.close()
    all_handles = driver.window_handles
    now_handle = all_handles[-1]
    driver.switch_to.window(now_handle)






# # Close browser once task is completed
# driver.quit()








# This small scraper aims to scrape relative data of sponser relatives. 
#
#
# Initiation
from selenium import webdriver
from time import sleep
import os
from bs4 import BeautifulSoup
import requests


if __name__ == '__main__': 

    # Open up a Firefox browser and navigate to web page. 
    driver = webdriver.Chrome()
    driver.get("http://exam.sac.net.cn/pages/registration/sac-publicity-report.html")
    # I put sleep here so that the page would be loaded fully. It happened before that only a small portion of rows were loaded. 
    sleep(5)


    # We start form the first row, which corresponds to the first organization. 
    nuOfCurrentRow = 1


    while (nuOfCurrentRow <= 121): 

        # In this part, we would go through each row and get the name of each organization. 
        # The name of the organization is stored in org_name
        # The row we are looking at is nuOfCurrentRow
        org_name = driver.find_element_by_xpath("""/html/body/div/table[3]/tbody[2]/tr[%d]/td[2]""" % nuOfCurrentRow).text
        print(org_name)


        # Now we would click on the link to jump to the list that has all the information of the sponsers. 
        driver.find_element_by_xpath("""/html/body/div/table[3]/tbody[2]/tr[%d]/td[10]/a""" % nuOfCurrentRow).click()


        # Get all the handles of open pages
        all_handles = driver.window_handles


        # Switch to the page we just opened
        now_handle = all_handles[1]
        driver.switch_to.window(now_handle)


        # Now we would like to get the url of this page. And ... at least get some basic imformation of this window, like how many pages are listed for this organization. 
        currentUrl = driver.current_url
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        nuOfPages_text = soup.find("span", id="sp_1").text
        nuOfPages = int(nuOfPages_text)
        print(nuOfPages)


        # We start from page 1. 
        nuOfCurrentPage = 1


        while (nuOfCurrentPage <= nuOfPages): 
            print(nuOfCurrentPage)
            sleep(3)
            

            # In this loop, we would open the links on this page one by one. After each iteration, we would close the window we just opened and then return to the previous window. 
            for loop_num in range(1, 100): 
                # Click on the page we just opened
                driver.find_element_by_xpath("""//*[@id="%s"]/td[2]/a""" % loop_num).click()
                all_handles = driver.window_handles
                now_handle = all_handles[2]
                driver.switch_to.window(now_handle)


                # Then we do some scraping here. Now we would like to close this window and go for the next window. 
                # Scraping
                # ...
                # ...
                # ...
                # ...
                sleep(2)


                #Close the current window and go back to the previous window
                driver.close()
                all_handles = driver.window_handles
                now_handle = all_handles[-1]
                driver.switch_to.window(now_handle)
            

            # We would click here to go to the next page. 
            driver.find_element_by_css_selector(".ui-icon.ui-icon-seek-next").click()
            

            # After getting to the next page, current page number should plus 1. Then we would go back to the start of this while loop. 
            nuOfCurrentPage = nuOfCurrentPage + 1



        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])


        nuOfCurrentRow = nuOfCurrentRow + 1






    # # Close browser once task is completed
    # driver.quit()








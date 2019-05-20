# This small scraper aims to scrape relative data of sponser relatives. 
#
#
# Initiation
from selenium import webdriver
from time import sleep
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.request
import pandas as pd


# This function would scrap the information of the sponser from the last layer
def scrapInfo(org_name): 


    # Now we try to extract the table out of the page with BeautifulSoup
    html_sponsor = driver.page_source
    soup_sponsor = BeautifulSoup(html_sponsor, "lxml")

    
    sponser_name = soup_sponsor.findAll("td")[2].text
    print("Scraping the information of ", sponser_name)


    # Assign the name the organization to variable current_org
    current_org = org_name


    table = soup_sponsor.findAll("table")[-1]
    table_rows = table.findAll("tr")

    l = []
    for tr in table_rows: 
        td = tr.findAll("td")
        row = [tr.text for tr in td]
        l.append(row)


    l = l[2:]
    # Transfer l to a dataframe
    df = pd.DataFrame(l, columns = ["ID", "date_certificate", "org", "position", "status", "filing_date"])
    df['current_org'] = current_org
    df['sponser_name'] = sponser_name


    # Download and rename the picture
    img = soup_sponsor.findAll('img')[1]
    imgUrlSeg = img['src']
    imgUrlTail = imgUrlSeg[6:]
    imgUrl = "http://exam.sac.net.cn/" + imgUrlTail
    imgFilePath = current_org + "_" + sponser_name + ".jpg"
    urllib.request.urlretrieve(imgUrl, imgFilePath)
    # os.rename("a.jpg", str(current_org) + '_' + str(sponser_name) + '.jpg')

    return df



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
        print("We are currently dealing with sponsors from " + org_name)


        # Now we would click on the link to jump to the list that has all the information of the sponsers. 
        driver.find_element_by_xpath("""/html/body/div/table[3]/tbody[2]/tr[%d]/td[10]/a""" % nuOfCurrentRow).click()


        # Get all the handles of open pages
        all_handles = driver.window_handles


        # Switch to the page we just opened
        now_handle = all_handles[1]
        driver.switch_to.window(now_handle)


        # Now we would like to get the url of this page. And ... at least get some basic imformation of this window, like how many pages are listed for this organization. 
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        nuOfPages_text = soup.find("span", id="sp_1").text
        nuOfPages = int(nuOfPages_text)
        print(nuOfPages, " page(s) for this organization")


        # We start from page 1. 
        nuOfCurrentPage = 1


        df_org = pd.DataFrame(columns = ['ID', 'date_certificate', 'org', 'position', 'filing_date', 'current_org', 'sponser_name'])


        while (nuOfCurrentPage <= nuOfPages): 
            print("We are currently on page", nuOfCurrentPage)
            sleep(3)


            nuOfSponsers_seg = driver.find_element_by_xpath("""//*[@id="pager_right"]/div""").text()
            nuOfSponsers = nuOfSponsers_seg.split(" ")[-2]
            print(nuOfSponsers, " sponser(s) on this page")
            

            # In this loop, we would open the links on this page one by one. After each iteration, we would close the window we just opened and then return to the previous window. 
            loop_num = 1
            while (loop_num <= int(nuOfSponsers)): 
                # Click on the page we just opened
                driver.find_element_by_xpath("""//*[@id="%s"]/td[2]/a""" % loop_num).click()
                all_handles = driver.window_handles
                now_handle = all_handles[2]
                driver.switch_to.window(now_handle)


                currentUrl = driver.current_url
                
                
                # Then we do some scraping here with the function scrapInfo()
                df_sponsor = scrapInfo(org_name)
                sleep(2)
                df_org = df_org.append(df_sponsor, ignore_index=True)



                #Close the current window and go back to the previous window
                driver.close()
                sleep(2)
                all_handles = driver.window_handles
                now_handle = all_handles[-1]
                driver.switch_to.window(now_handle)

                loop_num += 1
            

            # We would click here to go to the next page. 
            driver.find_element_by_css_selector(".ui-icon.ui-icon-seek-next").click()
            

            # After getting to the next page, current page number should plus 1. Then we would go back to the start of this while loop. 
            nuOfCurrentPage += 1

            excel_name = org_name + ".xlsx"
            df_org.to_excel(excel_name, index = False)



        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])


        nuOfCurrentRow = nuOfCurrentRow + 1



    # Close browser once task is completed
    driver.quit()








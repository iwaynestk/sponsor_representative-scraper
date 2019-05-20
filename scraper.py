# This small scraper aims to scrape relative data of sponser relatives. 
#
#


# Initiation
from selenium import webdriver
from time import sleep
import os
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import pandas as pd
import random
import string
import zipfile


# This function would scrap the information of the sponser from the last layer
def scrapInfo(org_name): 


    # Now we try to extract the table out of the page with BeautifulSoup
    html_sponsor = driver.page_source
    soup_sponsor = BeautifulSoup(html_sponsor, "lxml")


    sleep(random.uniform(2.3, 6.5))
    sponser_name = soup_sponsor.findAll("td")[2].text
    print("Scraping the information of ", sponser_name)


    # Assign the name the organization to variable current_org
    current_org = org_name


    # Locate the big chunky table
    table = soup_sponsor.findAll("table")[-1]
    table_rows = table.findAll("tr")


    # Go over this table and fill the information in each row into 'l'
    l = []
    for tr in table_rows: 
        td = tr.findAll("td")
        row = [tr.text for tr in td]
        l.append(row)


    # Throw away the first 2 rows of 'l'
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


    # # 代理服务器
    # proxyHost = "http-dyn.abuyun.com"
    # proxyPort = "9020"

    # # 代理隧道验证信息
    # proxyUser = "HD3H9MO48ZJZ917D"
    # proxyPass = "0F1A23458DAC4C5C"

    # def create_proxy_auth_extension(proxy_host, proxy_port,
    #                                proxy_username, proxy_password,
    #                                scheme='http', plugin_path=None):
    #     if plugin_path is None:
    #         plugin_path = r'./{}_{}@http-dyn.abuyun.com_9020.zip'.format(proxy_username, proxy_password)

    #     manifest_json = """
    #     {
    #         "version": "1.0.0",
    #         "manifest_version": 2,
    #         "name": "Abuyun Proxy",
    #         "permissions": [
    #             "proxy",
    #             "tabs",
    #             "unlimitedStorage",
    #             "storage",
    #             "<all_urls>",
    #             "webRequest",
    #             "webRequestBlocking"
    #         ],
    #         "background": {
    #             "scripts": ["background.js"]
    #         },
    #         "minimum_chrome_version":"22.0.0"
    #     }
    #     """

    #     background_js = string.Template(
    #         """
    #         var config = {
    #             mode: "fixed_servers",
    #             rules: {
    #                 singleProxy: {
    #                     scheme: "${scheme}",
    #                     host: "${host}",
    #                     port: parseInt(${port})
    #                 },
    #                 bypassList: ["foobar.com"]
    #             }
    #           };

    #         chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    #         function callbackFn(details) {
    #             return {
    #                 authCredentials: {
    #                     username: "${username}",
    #                     password: "${password}"
    #                 }
    #             };
    #         }

    #         chrome.webRequest.onAuthRequired.addListener(
    #             callbackFn,
    #             {urls: ["<all_urls>"]},
    #             ['blocking']
    #         );
    #         """
    #     ).substitute(
    #         host=proxy_host,
    #         port=proxy_port,
    #         username=proxy_username,
    #         password=proxy_password,
    #         scheme=scheme,
    #     )

    #     with zipfile.ZipFile(plugin_path, 'w') as zp:
    #         zp.writestr("manifest.json", manifest_json)
    #         zp.writestr("background.js", background_js)

    #     return plugin_path

    # proxy_auth_plugin_path = create_proxy_auth_extension(
    #     proxy_host=proxyHost,
    #     proxy_port=proxyPort,
    #     proxy_username=proxyUser,
    #     proxy_password=proxyPass)

    # option = webdriver.ChromeOptions()

    # option.add_argument("--start-maximized")
    # option.add_extension(proxy_auth_plugin_path)

    # driver = webdriver.Chrome(chrome_options=option)




    # # Open up a Chrome browser and navigate to web page. 
    # driver = webdriver.Chrome()


    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
    driver = webdriver.Chrome(chrome_options=options)



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


        # Switch to the window we just opened
        driver.switch_to.window(driver.window_handles[-1])
        sleep(random.uniform(2.2, 5.8))


        # Now let's see how many sponsors are listed for this organization
        nuOfPages_text = driver.find_element_by_xpath("""//*[@id="sp_1"]""").text
        nuOfPages = int(nuOfPages_text)
        print(nuOfPages, " page(s) for this organization")


        # We start from page 1. 
        nuOfCurrentPage = 1


        # Create an empty dataframe with default column names
        df_org = pd.DataFrame(columns = ['ID', 'date_certificate', 'org', 'position', 'filing_date', 'current_org', 'sponser_name'])


        while (nuOfCurrentPage <= nuOfPages): 
            print("We are currently on page", nuOfCurrentPage)


            nuOfSponsers_seg = driver.find_element_by_xpath("""//*[@id="pager_right"]/div""").text
            nuOfSponsers = nuOfSponsers_seg.split(" ")[-2]
            print(nuOfSponsers, " sponser(s) on this page")
            

            # In this loop, we would open the links on the page of this organization one by one. After each iteration, we would close the window we just opened and then return to the previous window. 
            loop_num = 1
            while (loop_num <= int(nuOfSponsers)): 

                # Click on the page we just opened to see the detailed information of this specific sponser
                driver.find_element_by_xpath("""//*[@id="%s"]/td[2]/a""" % loop_num).click()
                driver.switch_to.window(driver.window_handles[2])
                
                
                # Then we do some scraping here with the function scrapInfo()
                sleep(random.uniform(5.1, 15.7))
                df_sponsor = scrapInfo(org_name)
                df_org = df_org.append(df_sponsor, ignore_index=True)


                #Close the current window and go back to the previous window
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])

                loop_num += 1
            

            sleep(300)
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


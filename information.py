# This file is a seperate program which would extract the information from the last layer. 


from selenium import webdriver
from time import sleep
import os
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options



# def scrapeInfo(url): 


#     # Get the name first
#     opts = Options()
#     opts.add_argument("user-agent=whatever you want")
#     driver = webdriver.Chrome(chrome_options=opts)
#     sleep(2)
#     driver.get(url)
#     sponserName = driver.find_element_by_xpath("""//*[@id="RPI_NAME"]""")
#     print(sponserName.text)


#     # Now we try to extract the table out of the page with BeautifulSoup
#     html_sponsor = driver.page_source
#     soup_sponsor = BeautifulSoup(html_sponsor, "lxml")
#     table_sponsor = soup_sponsor.find("tbody", id="publicityList")
#     print(table_sponsor)



    


# url = "http://exam.sac.net.cn/pages/registration/sac-finish-person.html?r2SS_IFjjk=88F25848CAB4167BE053D651A8C0611C"
# scrapeInfo(url)

html_path = "C:/Users/iwayn/Developer/py_spiders/sac-finish-person.html"
html_file = open(html_path, 'r', encoding = 'utf-8')
htmlhandle = html_file.read()
soup = BeautifulSoup(htmlhandle, 'lxml')

table = soup.findAll("table")[-1]
table_rows = table.findAll("tr")

l = []
for tr in table_rows: 
    td = tr.findAll("td")
    row = [tr.text for tr in td]
    l.append(row)


l = l[2:]
df = pd.DataFrame(l, columns = ["ID", "date_certificate", "org", "position", "status", "filing_date"])
print(df)
# This file is a seperate program which would extract the information from the last layer. 


from selenium import webdriver
from time import sleep
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd


def scrapeInfo(url): 


    # Get the name first
    driver = webdriver.Chrome()
    driver.get(url)
    sponserName = driver.find_element_by_xpath("""//*[@id="RPI_NAME"]""")
    print(sponserName.text)


    


url = "http://exam.sac.net.cn/pages/registration/sac-finish-person.html?r2SS_IFjjk=88F25848CAB4167BE053D651A8C0611C"
scrapeInfo(url)
# This function would only go once. 
# All the exceptions would be recorded in the file "exception.xlsx"
# You may run the script "deal_exception.xlsx" to fetch the img, info and work history of sponsors we missed. 
import json
import urllib.request
from urllib import parse
import requests
from time import sleep
import pandas as pd


# Headers settings for all requests command. 
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "exam.sac.net.cn", 
    "Origin": "http://exam.sac.net.cn", 
    "X-Requested-With": "XMLHttpRequest"
}

#####################################
# These are proxy settings. They will expire after 20/05/2019. 
# If you want to use similar proxy settings, you should change proxy server and tunnel settings. 
# Proxy server
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# Proxy tunnel
proxyUser = "H70GG67P8L53S52D"
proxyPass = "C2CC5B7F331CBB59"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host" : proxyHost,
    "port" : proxyPort,
    "user" : proxyUser,
    "pass" : proxyPass,
}

proxies = {
    "http"  : proxyMeta,
    "https" : proxyMeta,
}
# End of proxy settings
#####################################


# This function get the number of pages for an org based on the number of sponsors listed. 
def get_nu_of_pages(nu_sponsor):
    if (nu_sponsor % 100 == 0): 
        nu_of_pages = nu_sponsor / 100
    else: 
        nu_of_pages = (nu_sponsor // 100) + 1
    return nu_of_pages


# This function would return a list of all the sponsors in the same org with their basic info
# such as name, certificate ...
def get_info_of_org(org_info): 

    org_url = "http://exam.sac.net.cn/pages/registration/train-line-register!list.action"

    nu_of_pages = get_nu_of_pages(org_info["nu_sponsor"])
    print("There are ", nu_of_pages, " pages for this org")

    current_page = 1
    org_list = []
    while (current_page <= nu_of_pages): 
        org_post_data = {
            "filter_EQS_AOI_ID": org_info["org_ID"], 
            "filter_EQS_PTI_ID": "6", 
            "page.searchFileName": "homepage", 
            "page.sqlKey": "PAGE_FINISH_PUBLICITY", 
            "page.sqlCKey": "SIZE_FINISH_PUBLICITY", 
            "_search": "false", 
            "page.pageSize": "100", 
            "page.pageNo": current_page, 
            "page.orderBy": "id", 
            "page.order": "desc"
        }
    
        org_req = requests.post(url = org_url, data = org_post_data, headers = headers, proxies = proxies)
        org_data = org_req.json()
        org_result = org_data["result"]
        for sponsor in org_result: 
            d = {}
            d["sponsor_PPP_ID"] = sponsor["PPP_ID"]
            d["sponsor_name"] = sponsor["RPI_NAME"]
            d["sponsor_org"] = sponsor["AOI_NAME"]
            d["sponsor_certificate"] = sponsor["CER_NUM"]
            org_list.append(d)

        sleep(4)

        current_page += 1

    file_org = org_info["org_name"] + ".xlsx"
    df_org = pd.DataFrame(org_list)
    df_org.to_excel(file_org, index = False)

    return org_list


# This function would return the RPI ID of a sponsor
# RPI ID is used to fetch the detailed info of a sponsor. 
def get_RPI_ID(sponsor_info): 

    sponsor_post_data_PPP = {
        "filter_EQS_PPP_ID": sponsor_info["sponsor_PPP_ID"], 
        "sqlkey": "registration", 
        "sqlval": "SD_A02Leiirkmuexe_b9ID"
    }

    sponsor_PPP_url  = "http://exam.sac.net.cn/pages/registration/train-line-register!gsUDDIsearch.action"
    sponsor_PPP_req = requests.post(url = sponsor_PPP_url, data = sponsor_post_data_PPP, headers = headers, proxies = proxies)
    RPI_ID = sponsor_PPP_req.json()[0]["RPI_ID"]

    return RPI_ID


# This function would return the work history table of a sponsor. 
def get_hist_table(RPI_ID, sponsor_name):

    sponsor_post_data_RPI = {
        "filter_EQS_RH#RPI_ID": RPI_ID, 
        "sqlkey": "registration", 
        "sqlval": "SEARCH_LIST_BY_PERSONWWCX"
    }

    sponsor_RPI_work_history_url = "http://exam.sac.net.cn/pages/registration/train-line-register!gsUDDIsearch.action"
    sponsor_history_req = requests.post(url = sponsor_RPI_work_history_url, data = sponsor_post_data_RPI, headers = headers, proxies = proxies)
    sponsor_history_data = sponsor_history_req.json()
    for item in sponsor_history_data: 
        item.update({"sponsor_name": sponsor_name})

    return sponsor_history_data


# This function would get the image of a sponsor based on his RPI ID. 
def get_image(RPI_ID):  

    image_post_data = {
        "filter_EQS_RPI_ID": RPI_ID, 
        "sqlkey": "registration", 
        "sqlval": "SELECT_PERSON_INFO"
    }

    image_page_url = "http://exam.sac.net.cn/pages/registration/train-line-register!gsUDDIsearch.action"
    image_req = requests.post(url = image_page_url, data = image_post_data, headers = headers, proxies = proxies)
    image_data = image_req.json()
    image_url = "http://exam.sac.net.cn/photo/images/" + image_data[0]["RPI_PHOTO_PATH"]
    print(image_url)
    image_name = image_data[0]["AOI_NAME"] + "_" + image_data[0]["RPI_NAME"] + ".jpg"
    urllib.request.urlretrieve(image_url, image_name)



# Extract main list from the website and write it to file "main_info.txt"
def get_main_info(): 
    main_url = "http://exam.sac.net.cn/pages/registration/train-line-register!orderSearch.action"

    main_post_data = {
        "filter_EQS_OTC_ID": "10", 
        "ORDERNAME": "AOI#AOI_NAME", 
        "ORDER": "ASC", 
        "sqlkey": "registration", 
        "sqlval": "SELECT_LINE_PERSON"
    }

    main_req = requests.post(url = main_url, data = main_post_data, headers = headers, proxies = proxies)
    main_data = main_req.json()

    main_data_list = []
    for org in main_data: 
        d = {}
        d["org_ID"] = org["AOI_ID"]
        d["org_name"] = org["AOI_NAME"]
        d["nu_sponsor"] = int(org["PTI6PERSON"])
        main_data_list.append(d)

    df_main = pd.DataFrame(main_data_list)
    df_main.to_excel("main_info.xlsx", index = False)

    return main_data_list


if __name__ == "__main__": 
    
    main_data_list = get_main_info()
    exception_list = []
    for org in main_data_list: 

        print("Checking out ", org["org_name"])
        try: 
            sponsors = get_info_of_org(org)
        except Exception: 
            print("Getting information of org ", org["org_name"], " failed. Moving on to the next one. ")
            continue

        work_hist = []

        for sponsor in sponsors: 
            try: 
                RPI_ID = get_RPI_ID(sponsor)
                print("Checking out sponsor: ", sponsor["sponsor_name"], " RPI_ID: ", RPI_ID)
                work_hist = work_hist + get_hist_table(RPI_ID, sponsor["sponsor_name"])
                get_image(RPI_ID)

            except Exception as e: 
                print(e)
                print("Having trouble when dealing with data of ", sponsor["sponsor_name"], " from ", org["org_name"])
                exception_list.append(sponsor)
                sleep(2)
                continue


        # Write the whole work hist of this org
        file_org_detailed = org["org_name"] + "_detailed.xlsx"
        df_org_detailed = pd.DataFrame(work_hist)
        df_org_detailed.to_excel(file_org_detailed, index = False)

    # Write all the exceptions into a single file
    df_exception = pd.DataFrame(exception_list)
    df_exception.to_excel("exception.xlsx", index = False)






import json
import urllib.request
from urllib import parse
import requests
from time import sleep


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "exam.sac.net.cn", 
    "Origin": "http://exam.sac.net.cn"
}

def get_nu_of_pages(nu_sponsor):
    if (nu_sponsor % 100 == 0): 
        nu_of_pages = nu_sponsor / 100
    else: 
        nu_of_pages = (nu_sponsor // 100) + 1
    return nu_of_pages


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
    
        org_req = requests.post(url = org_url, data = org_post_data, headers = headers)
        org_data = org_req.json()
        org_result = org_data["result"]
        for sponsor in org_result: 
            d = {}
            d["sponsor_ID"] = sponsor["PPP_ID"]
            d["sponsor_name"] = sponsor["RPI_NAME"]
            d["sponsor_org"] = sponsor["AOI_NAME"]
            d["sponsor_certificate"] = sponsor["CER_NUM"]
            org_list.append(d)

        sleep(4)

        current_page += 1

    file_org = org_info["org_name"] + ".txt"

    with open(file_org, "w", encoding='utf-8') as orgout: 
        json.dump(org_list, orgout, ensure_ascii = False)





# Extract main list from the website and write it to file "main_info.txt"

main_url = "http://exam.sac.net.cn/pages/registration/train-line-register!orderSearch.action"

main_post_data = {
    "filter_EQS_OTC_ID": "10", 
    "ORDERNAME": "AOI#AOI_NAME", 
    "ORDER": "ASC", 
    "sqlkey": "registration", 
    "sqlval": "SELECT_LINE_PERSON"
}

main_req = requests.post(url = main_url, data = main_post_data, headers = headers)
main_data = main_req.json()

main_data_list = []
for org in main_data: 
    d = {}
    d["org_ID"] = org["AOI_ID"]
    d["org_name"] = org["AOI_NAME"]
    d["nu_sponsor"] = int(org["PTI6PERSON"])
    main_data_list.append(d)

# with open("main_info.txt", "w", encoding='utf-8') as fout: 
#     json.dump(main_data_list, fout, ensure_ascii = False)

for org in main_data_list: 
    try: 
        print("Checking out ", org["org_name"])
        get_info_of_org(org)
    except Exception as e: 
        print(e)
        continue









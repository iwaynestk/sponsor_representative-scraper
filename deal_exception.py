# Run this script after you have run "main.py"
# It would fetch the info and imgs we missed out

import json
import requests
import pandas as pd
import urllib.request

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



# This function would return the RPI ID of a sponsor
# RPI ID is used to fetch the detailed info of a sponsor.
def get_RPI_ID(PPP_ID): 

    sponsor_post_data_PPP = {
        "filter_EQS_PPP_ID": PPP_ID, 
        "sqlkey": "registration", 
        "sqlval": "SD_A02Leiirkmuexe_b9ID"
    }

    sponsor_PPP_url  = "http://exam.sac.net.cn/pages/registration/train-line-register!gsUDDIsearch.action"
    sponsor_PPP_req = requests.post(url = sponsor_PPP_url, data = sponsor_post_data_PPP, headers = headers, proxies = proxies)
    RPI_ID = sponsor_PPP_req.json()[0]["RPI_ID"]

    return RPI_ID

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


# Read all the exceptions and we only take two columns. 
# They are "sponsor_PPP_ID" and "sponsor_name"
df_exception = pd.read_excel("exception.xlsx")
df_exception_seg = df_exception[["sponsor_PPP_ID", "sponsor_name"]]
exception_list = df_exception_seg.to_dict(orient = "records")

# PPP_ID_list would be used to fetched a list of RPI ID
PPP_ID_list = df_exception["sponsor_PPP_ID"].tolist()

RPI_ID_list = []
PPP_ID_list_copy = PPP_ID_list

# We would keep looping until all the RPI IDs are fetched. 
while True: 
    for PPP_ID in PPP_ID_list: 
        try: 
            RPI_ID_list.append(get_RPI_ID(PPP_ID))
            PPP_ID_list_copy.remove(PPP_ID)
            print("Done with ", PPP_ID)

        except: 
            print("Unable to fetch RPI ID of ", PPP_ID)
            continue

    PPP_ID_list = PPP_ID_list_copy
    if (len(PPP_ID_list) == 0): 
        break

print("All RPI ID fetched! ")
df_RPI = pd.DataFrame(RPI_ID_list)
df_RPI.to_excel("RPI_exception.xlsx", index = False)


RPI_ID_list_copy_image = RPI_ID_list

# Fetch all the images. 
# Sometimes the image may not exist. WHen it happens, there would be some exception about connection. 
# We would then directly go to the next loop. 
for RPI_ID in RPI_ID_list: 
    try: 
        get_image(RPI_ID)
        RPI_ID_list_copy_image.remove(RPI_ID)
        print("Successfully get image of RPI ID: ", RPI_ID)
    except: 
        print("Unable to fetch image of RPI ID: ", RPI_ID)
        continue
print("All images fetched! ")


# Now fetch the work history
# Keep looping until all the work hist info is fetched. 
print("Starting: fetch work history info")
work_hist = []
exception_list_copy = exception_list
while True: 
    for sponsor in exception_list: 
        try: 
            RPI_ID = get_RPI_ID(sponsor["sponsor_PPP_ID"])
            work_hist = work_hist + get_hist_table(RPI_ID, sponsor["sponsor_name"])
            exception_list_copy.remove(sponsor)
            print("Successsfully fetched work history of: ", sponsor["sponsor_name"])
        except: 
            print("Unable to fetch work history of: ", sponsor["sponsor_name"])
            continue

    exception_list = exception_list_copy
    if (len(exception_list) == 0): 
        print("Successfully fetched all work history! ")
        break

print("work hist is: ", work_hist)
df_work_hist_exception = pd.DataFrame(work_hist)
df_work_hist_exception.to_excel("work_hist_exception.xlsx", index = False)
print("All work done. ")

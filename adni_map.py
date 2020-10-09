from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import pandas as pd
import glob
import shutil
import sh

try:
    # Webdriver Location
    PATH = input("Please enter the location of Chrome Webdriver:")
    PATH = PATH + "/chromedriver"
    # Download Location Path
    mypath_download = input("Please enter the desired download location:")
    # Username of ADNI
    email_key = input("Please enter the ADNI Username:")
    # Password of ADNI
    pw_key = input("Please enter the ADNI Password:")
    # Create Download Location
    mypath = mypath_download + "/adni_table"
    if not os.path.exists(mypath):
        os.makedirs(mypath)
        print("Temporary directory created in " + mypath)
except:
    print("Unexpected input")

try:
    # Open Chrome and Navigate to the Source
    print("Loading page ...")
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : mypath}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(PATH, options=chrome_options)
    driver.get("https://ida.loni.usc.edu/pages/access/studyData.jsp?categoryId=12")
    print("Filling login information ...")
    email = driver.find_element_by_name("userEmail")
    pw = driver.find_element_by_name("userPassword")
    email.send_keys(email_key)
    pw.send_keys(pw_key)
    pw.send_keys(Keys.RETURN)
    print("Navigating ...")
    link_pro = driver.find_element_by_link_text("PROJECTS")
    link_pro.click()
    link_adni = driver.find_element_by_link_text("ADNI")
    link_adni.click()
    link_dl = driver.find_element_by_link_text("DOWNLOAD")
    link_dl.click()
    link_sd = driver.find_element_by_link_text("Study Data")
    link_sd.click()
    link_td = driver.find_element_by_link_text("Test Data")
    link_td.click()
    link_all = driver.find_element_by_link_text("ALL")
    link_all.click()
    print("Getting list of tables ...")
    link_list = [];
    link_list = driver.find_elements_by_class_name("contentFont")
except:
    print("Fail to open page. Please check the webdriver and the login information")

try:
    # Download, Get Name, and Delete
    file_label = []
    file_name =[]
    for i in range(int(len(link_list)/2)):
        l_name = link_list[2*i].text
        if l_name in file_label:
            continue
        file_label.append(l_name)
        link = driver.find_element_by_link_text(l_name)
        link.click()
        print("(" + str(i+1) + "/" + str(int(len(range(int(len(link_list)/2))))) + ")" + " Downloading " + l_name + " ... ")
        while glob.glob(os.path.join(mypath, '*')) == []:
            time.sleep(1)
        time.sleep(1/2)
        all_name = glob.glob(os.path.join(mypath, '*'))
        for j in range(len(all_name)):
            if all_name[j].split(".")[-1] == "crdownload":
                head, tail = os.path.split(".".join(all_name[j].split(".")[:-1]))
                if tail not in file_name:
                    file_name.append(tail)
                    print("Added file name " + tail)
            else:
                head, tail = os.path.split(all_name[j])
                if tail not in file_name:
                    f_name = all_name[j]
                    file_name.append(tail)
                    print("Added file name " + tail)
        sh.rm(glob.glob(os.path.join(mypath, '*')))
except:
    print("Downloading error, please check the connection and try again")

try:
    # Output
    file_name_map = pd.DataFrame({"file_label": file_label, "file_name": file_name})
    print("Merge successfully,")
    shutil.rmtree(mypath, ignore_errors=True)
    print("Temporary directory deleted")
    file_name_map.to_csv(mypath_download+"/ADNI_map.csv")
    print("ADNI_map.csv created in " + mypath_download + "/ADNI_map.csv")
except:
    print("Fail to create the csv file")

# Quit Driver
driver.quit()
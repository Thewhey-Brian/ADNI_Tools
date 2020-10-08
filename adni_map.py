from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import pandas as pd
import glob
import shutil

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

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : mypath}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(PATH, options=chrome_options)
driver.get("https://ida.loni.usc.edu/pages/access/studyData.jsp?categoryId=12")
email = driver.find_element_by_name("userEmail")
pw = driver.find_element_by_name("userPassword")
email.send_keys(email_key)
pw.send_keys(pw_key)
pw.send_keys(Keys.RETURN)
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
link_list = [];
link_list = driver.find_elements_by_class_name("contentFont")

file_label = []
file_name =[]
# range(int(len(link_list)/2))
for i in range(int(len(link_list)/2)):
    l_name = link_list[2*i].text
    file_label.append(l_name)
    link = driver.find_element_by_link_text(l_name)
    link.click()
    print("Downloading " + l_name + " ...")
    while glob.glob(mypath + "/*.csv") == [] and glob.glob(mypath + "/*") != []:
        time.sleep(3)
    print(l_name + " Downloaded")
    f_name = glob.glob(mypath + "/*.csv")[0]
    head, tail = os.path.split(f_name)
    file_name.append(tail)
    print("File name " + tail + " added")
    os.remove(f_name)
    print(l_name + " Deleted")

file_name_map = pd.DataFrame({"file_label": file_label, "file_name": file_name})
shutil.rmtree(mypath, ignore_errors=True)
file_name_map.to_csv(mypath_download+"/ADNI_map.csv")
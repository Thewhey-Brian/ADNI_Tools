from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import pandas as pd
import glob
import os
import shutil
import sh
import subprocess

try:
    # Webdriver Location
    PATH = input("Please enter the location of Chrome Webdriver: ")
    PATH = PATH + "/chromedriver"
    # Download Location Path
    mypath_download = input("Please enter the desired download location: ")
    # Username of ADNI
    email_key = input("Please enter the ADNI Username: ")
    # Password of ADNI
    pw_key = input("Please enter the ADNI Password: ")
    # Create Download Location
    mypath = mypath_download + "/adni_table"
    if not os.path.exists(mypath):
        os.makedirs(mypath)
        print("Temporary directory created in " + mypath)
except:
    print("Unexpected input")

def clean_tr(path, bar): 
    now = time.time()
    files = [os.path.join(path, filename) for filename in os.listdir(path)]
    for filename in files:
        if (now - os.stat(filename).st_mtime) < bar:
            if os.path.isdir(files[0]): shutil.rmtree(filename)
            else: os.remove(filename)
                
def delet_file(path, filename): 
    file = path + filename
    if os.path.isdir(file): shutil.rmtree(file)
    else: os.remove(file)
            
def cancel_dl(): 
    driver.switch_to.window(driver.window_handles[1])
    driver.execute_script("document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('cr-button[focus-type=\x22cancel\x22]').click()")
    driver.switch_to.window(driver.window_handles[0])

def check_bl(path, bar):
    bar = 0
    while glob.glob(os.path.join(path, '*')) == []:
        bar = bar + 1
        time.sleep(2)
        if bar > bar: 
            return True

def wait_dl(path, suffix, bar):
    for i in range(bar):
        time.sleep(1)
        try: 
            if glob.glob(os.path.join(path, '*'))[0].split(".")[-1] != suffix:
                return False
        except:
            time.sleep(1)
    return True

try:
    # Open Chrome and Navigate to the Source
    print("Loading page ...")
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
    driver.find_element_by_link_text("PROJECTS").click()
    driver.find_element_by_link_text("ADNI").click()
    driver.find_element_by_link_text("DOWNLOAD").click()
    driver.find_element_by_link_text("Study Data").click()
    driver.find_element_by_id("ygtvlabelel48").click()
    # get all contents under contentFont class; even-link, odd-version
    info_list = [];
    info_list = driver.find_elements_by_xpath("//td[@class='contentFont']")
    link_list = [];
    link_list = driver.find_elements_by_xpath("//td[@class='contentFont']/a")
    driver.execute_script('''window.open("http://bings.com","_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome://downloads')
    driver.switch_to.window(driver.window_handles[0])
    file_label = []
    file_name =[]
    file_vars = []
    file_version = []
    lar_file = []
    err_file = []
    time.sleep(3)
except:
    print("Fail to open page. Please check the webdriver and the login information")

try:
    for i in range(0, int(len(link_list)), 1):
        # Click each download links    
        l_name = link_list[i].text.replace('\n', '').strip()
        version = info_list[2*i+1].text.replace('  Version: ', '')
        file_label.append(l_name)
        file_version.append(version)
        try:
            link_list[i].click()
        except:
            pass
        print("(" + str(i) + "/" + str(int(len(link_list))) + ")" + "Downloading " + l_name + " ... ")
        # Check bad links
        time.sleep(1)
        if check_bl(mypath, 3):
            file_name.append('')
            file_vars.append('')
            err_file.append(l_name)
            print('Bad link')
            continue
        # Wait for downloading
        timeout = wait_dl(mypath, "crdownload", 60)
        # large file
        if timeout: 
            name = glob.glob(os.path.join(mypath, '*'))
            cancel_dl()
            head, tail = os.path.split(name[0])
            file_name.append(tail.replace('.crdownload', ''))
            file_vars.append('large')
            lar_file.append(l_name)
            print("Skip the large file ...")
            continue
        # classify downloaded file type and add values
        time.sleep(2)
        name = glob.glob(os.path.join(mypath, '*'))
        head, tail = os.path.split(name[0])
        file_name.append(tail)
        print("Added file name " + tail)
        # directory
        if len(name[0].split(".")) < 2 or os.path.isdir(name[0]):
            file_vars.append('non-attributed/large')
            err_file.append(l_name)
            shutil.rmtree(name[0])
            time.sleep(1)
            print("Removed non-attributed/large file.")
            continue
        # non-csv file
        if tail.split(".")[-1] != "csv":
            file_vars.append('non-csv')
            err_file.append(l_name)
            os.remove(name[0])
            time.sleep(1)
            print("Removed non-csv file.")
            continue
        # csv file    
        try:
            file_vars.append(pd.read_csv(name[0]).columns.values.tolist())
            print("Variables added")
        except:
            file_vars.append('not avaliable')
            print("Variables not avaliable")
        os.remove(name[0])
        time.sleep(1) 
        print("Removed file.")    
except:
    print("Downloading error, please check the connection and try again")

try:
    # Output
    file_name_map = pd.DataFrame({"file_label": file_label, 
                                  "file_name": file_name, 
                                  "file_version": file_version, 
                                  "vars": file_vars})
    print("Merge successfully,")
    shutil.rmtree(mypath, ignore_errors=True)
    print("Temporary directory deleted")
    file_name_map.to_csv(mypath_download+"/ADNI_map.csv")
    print("ADNI_map.csv created in " + mypath_download + "/ADNI_map.csv")
except:
    print("Fail to create the csv file")

# Quit Driver
driver.quit()
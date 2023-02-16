from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
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
import getpass

try:
    # Download Location Path
    mypath_download = input("Please enter the desired download location: ")
    # Username of ADNI
    email_key = input("Please enter the ADNI Username: ")
    # Password of ADNI
    pw_key = getpass.getpass("Please enter the ADNI Password: ")
    # Create Download Location
    mypath = mypath_download + "/adni_table"
    if not os.path.exists(mypath):
        os.makedirs(mypath)
        print("Temporary directory created in " + mypath)
except:
    print("Unexpected inputs.")

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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://ida.loni.usc.edu/login.jsp")
    print("Webpage opened.")
    time.sleep(6)
    driver.find_element(By.CLASS_NAME, "ida-cookie-policy-accept").click()
    print("Cookie accepted.")
    time.sleep(6)
    driver.find_element(By.CLASS_NAME, "ida-user-menu-icon").click()
    time.sleep(2)
    email = driver.find_element(By.NAME, "userEmail")
    pw = driver.find_element(By.NAME, "userPassword")
    email.send_keys(email_key)
    pw.send_keys(pw_key)
    pw.send_keys(Keys.RETURN)
    print("Login information entered.")
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "download").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div[4]/div[2]/div/div[1]/span").click()
    driver.find_element(By.ID, "ygtvlabelel48").click()
    print("Directed to data downloading page.")
    info_list = [];
    info_list = driver.find_elements(By.XPATH, "//td[@class='contentFont']")
    link_list = [];
    link_list = driver.find_elements(By.XPATH, "//td[@class='contentFont']/a")
    driver.execute_script('''window.open("http://google.com","_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome://downloads')
    driver.switch_to.window(driver.window_handles[0])
    print("Loaded download page.")
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
        if "PDF" in l_name or "Methods" in l_name or "Documentation" in l_name or "Document" in l_name or "METHODS" in l_name or "About" in l_name:
            file_name.append('')
            #file_vars.append('')
            file_vars.append('Methods file.')
            time.sleep(1)
            print("Skip methods file.")
            continue
        try:
            link_list[i].click()
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, "preparing-download-close-btn").click()
        except:
            pass
        print("(" + str(i) + "/" + str(int(len(link_list))) + ")" + "Downloading " + l_name + " ... ")
        # Check bad links
        time.sleep(2)
        if check_bl(mypath, 3):
            file_name.append('')
            file_vars.append('')
            err_file.append(l_name)
            print('Bad link')
            continue
        # Check pop-ups
        time.sleep(3)
        if len(driver.window_handles) > 2: 
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[2])
            time.sleep(1)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            file_name.append('')
            file_vars.append('webpage_pdf')
            lar_file.append(l_name)
            print('Skip discription file ...')
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
                                  "vars": file_vars_tem})
    print("File merge successfully.")
    shutil.rmtree(mypath, ignore_errors=True)
    print("Temporary directory deleted.")
    file_name_map.to_csv(mypath_download+"/ADNI_map.csv")
    print("ADNI_map.csv created in " + mypath_download + "/ADNI_map.csv")
except:
    print("Fail to create the csv file")

# Quit Driver
driver.quit()

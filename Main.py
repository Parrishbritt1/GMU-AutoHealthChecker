# Goals: Create a bot that automates the GMU Health Check process 
# - Possibly making it an .exe or some way to make it more distributable
# How: Using webscraping to get html and make inputs that state I'm healthy
# Why: It's annoying to fill out the same answers every day and saving a whopping valuable 3 mins of my day lol

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from config import DRIVER_PATH, USERNAME, PASSWORD
import time


driver = webdriver.Chrome(executable_path=DRIVER_PATH)

driver.get("https://itsapps2.gmu.edu/symptom/Account/Login/")

# Click 'LOGIN WITH MASON NETID' button
login_with_NETID_ele = driver.find_element_by_id("gmulogin")
login_with_NETID_ele.click()

# Click field and enter username
username_ele = driver.find_element_by_id("username")
username_ele.click()
username_ele.send_keys(USERNAME)

# Click field and enter password
password_ele = driver.find_element_by_id("password")
password_ele.click()
password_ele.send_keys(PASSWORD)

# Click login
login_ele = driver.find_element_by_name("_eventId_proceed")
login_ele.click()

# -------------------------------DUO Authentication---------------------------------
frame = driver.find_element_by_id("duo_iframe")
driver.switch_to.frame(frame)

# Click remember for 14 days if not already selected
remember_14_days_ele = driver.find_element_by_xpath("/html/body/div/div/div[1]/div/form/div[2]/div/label/input")
if not remember_14_days_ele.is_selected():
    remember_14_days_ele.click()

# click passcode button
passcode_button_ele = driver.find_element_by_id("passcode")
passcode_button_ele.click()

# Enter 2SA passcode
while True:
    time.sleep(.5)
    duo_auth_passcode = input("Enter DUO Passcode: ")
    passcode_text_field_ele = driver.find_element_by_class_name("passcode-input")
    passcode_text_field_ele.click()
    passcode_text_field_ele.clear()
    passcode_text_field_ele.send_keys(duo_auth_passcode)

    login_button_ele = driver.find_element_by_id("passcode")
    login_button_ele.click()
    
    time.sleep(.5)
    # If error doesn't exist hence NoSuchElementException then break out of loop
    try:
        driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div[2]')
        
        # Untested - may print when not supposed to
        print("**Wrong Passcode**")
        print("May have to refresh code on DUO app")
    except NoSuchElementException:
        break


time.sleep(.5)
# Leave iframe
driver.switch_to.default_content()

# Start Health Risk Assessment button
start_assessment_ele = driver.find_element_by_class_name("input-group")
start_assessment_ele.click()


# Closes the browser
# driver.quit()
# Goals: Create a bot that automates the GMU Health Check process 
# - Possibly making it an .exe or some way to make it more distributable
# How: Using webscraping to get html and make inputs that state I'm healthy
# Why: It's annoying to fill out the same answers every day and saving a whopping valuable 3 mins of my day lol

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config import DRIVER_PATH, USERNAME, PASSWORD, PHONE_NUMBER
import time
from datetime import date


def click_by_id(id):
    ele = driver.find_element_by_id(id)
    if not ele.is_selected():
        ele.click()

    return ele

def click_by_name(name):
    ele = driver.find_element_by_name(name)
    if not ele.is_selected():
        ele.click()

    return ele

def send_input(ele, input):
    ele.send_keys(input)

driver = webdriver.Chrome(executable_path=DRIVER_PATH)

driver.get("https://itsapps2.gmu.edu/symptom/Account/Login/")

# Click 'LOGIN WITH MASON NETID' button
click_by_id("gmulogin")

# Click field and enter username
ele = click_by_id("username")
send_input(ele, USERNAME)

# Click field and enter password
ele = click_by_id("password")
send_input(ele, PASSWORD)

# Click login
click_by_name("_eventId_proceed")

# -------------------------------DUO Authentication---------------------------------
frame = driver.find_element_by_id("duo_iframe")
driver.switch_to.frame(frame)

# Click remember for 14 days if not already selected
remember_14_days_ele = driver.find_element_by_xpath("/html/body/div/div/div[1]/div/form/div[2]/div/label/input")
if not remember_14_days_ele.is_selected():
    remember_14_days_ele.click()

# click passcode button
click_by_id("passcode")

# Enter 2SA passcode
while True:
    time.sleep(.5)
    duo_auth_passcode = input("Enter DUO Passcode: ")
    passcode_text_field_ele = driver.find_element_by_class_name("passcode-input")
    passcode_text_field_ele.click()
    passcode_text_field_ele.clear()
    passcode_text_field_ele.send_keys(duo_auth_passcode)

    click_by_id("passcode")
    
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


# --------------------------- Screening Portion ---------------------------
# Do you currently have any of the following conditions that are NOT explained by seasonal 
# allergies, flu, or another health condition?
click_by_id("rb_q_97_c2")

# Have you tested positive for COVID-19 in the last 10 days?
click_by_id("rb_q_98_c2")

# Have you had any of the following symptoms in the last 24 hours 
# that are not explained by seasonal allergies or another health condition?
click_by_id("rb_q_100_c2")

# In the last 14 days, have you been in close contact (less than 6 feet for 15 minutes or more) with
# • Someone 2 days before or 10 days after they tested positive or were diagnosed with COVID-19, or
# • Someone who had/has COVID-19 symptoms and is currently waiting for COVID-19 test results?
click_by_id("rb_q_103_c2")

# Are you fully vaccinated – received the second dose of Pfizer, Moderna vaccine, one dose of J&J vaccine, 
# or World Health Organization (WHO) authorized vaccine more than 14 days ago?
click_by_id("rb_q_104_c1")

# Are you planning to come to campus or participate in an in person Mason activity today?
click_by_id("rb_q_131_c1")

# Have you been on a Mason campus/facility or participated in a Mason sponsored/associated activity today or in the past 14 days?
click_by_id("rb_q_101_c1")

# Click Calendar button and input in date
ele = click_by_id("q_102")
today = date.today()
send_input(ele, today.strftime("%m%d"))

# Are you a student living on campus? Residential students answer yes even if you are not currently on campus.
click_by_id("rb_q_105_c1")

# Have you arrived from traveling outside the United States in the last 10 days? 
click_by_id("rb_q_106_c2")

# Phone Number
phone_ele = click_by_id("q_109")
phone_ele.clear()
send_input(phone_ele, PHONE_NUMBER)
    
# Do you consent and authorize George Mason University (GMU) to conduct collection, 
# testing and analysis of samples from you for the purpose of an approved Coronavirus (COVID-19) test?
click_by_id("rb_q_128_c1")

# Closes the browser
# driver.quit()
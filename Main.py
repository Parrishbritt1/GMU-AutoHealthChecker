# Goals: Create a bot that automates the GMU Health Check process 
# - Possibly making it an .exe or some way to make it more distributable
# How: Using webscraping to get html and make inputs that state I'm healthy
# Why: It's annoying to fill out the same answers every day and saving a whopping valuable 3 mins of my day lol

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import DRIVER_PATH, USERNAME, PASSWORD


driver = webdriver.Chrome(executable_path=DRIVER_PATH)

driver.get("https://itsapps2.gmu.edu/symptom/Account/Login/")

# Click 'LOGIN WITH MASON NETID' button
login_with_NETID_element = driver.find_element_by_id("gmulogin")
login_with_NETID_element.click()

# Click field and enter username
username_element = driver.find_element_by_id("username")
username_element.click()
username_element.send_keys(USERNAME)

# Click field and enter password
password_element = driver.find_element_by_id("password")
password_element.click()
password_element.send_keys(PASSWORD)

# Click login
login_element = driver.find_element_by_name("_eventId_proceed")
login_element.click()

# Getting duo auth iframe
duo_iframe = driver.find_element_by_id("duo_iframe")
print(duo_iframe)



# Closes the browser
# driver.quit()
from genericpath import isfile
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def makeOutputDir():
    if (os.path.isdir("./Output")):
        pass
    else:
        os.mkdir("./Output")
def nameScreenshot(num):
    if(os.path.isfile("./Output/"+num+".png")):
        os.remove("./Output/"+num+".png")
    return "./Output/"+num+".png"
def welcoming():
    print("Welcome!\nPut the courses numbers that you want to check in file named 'courses.txt' at the same folder sperated by a comma.\nExample: 20141,20231,22592\nPress any key when the file is ready and LET THE MAGIC HAPPEN :)")
    input()
    if(not os.path.isfile("./courses.txt")):
        print("I can't find 'courses.txt', try again!")
        exit()

welcoming()
makeOutputDir()
coursesNo = open("courses.txt","r")
driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
driver.get("https://regnew.psut.edu.jo/ProposedCoursesPublic.aspx")

yearBox = driver.find_element_by_xpath('//*[@id="ddlStudyYear"]/option[2]')
yearBox.click()
semBox = driver.find_element_by_xpath('//*[@id="ddlStudySemister"]/option[2]')
semBox.click()
numbers = coursesNo.readline().split(",")

for number in numbers:
    searchButton = driver.find_element_by_xpath('//*[@id="btnSearch"]')
    courseNo = driver.find_element_by_xpath('//*[@id="tbCourseNo"]')
    courseNo.clear()
    courseNo.send_keys(number)
    searchButton.click()
    time.sleep(1)
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.ID, 'gvProposedCoursesSchedule'))
        WebDriverWait(driver, timeout).until(element_present)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        table = driver.find_element_by_xpath('//*[@id="gvProposedCoursesSchedule"]')
        table.screenshot(nameScreenshot(number))
    except TimeoutException:
        print("Timed out waiting for page to load, try again!")
driver.close()
print("Done! check the output folder.")
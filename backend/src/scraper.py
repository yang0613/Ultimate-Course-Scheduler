from lib2to3.pgen2.driver import Driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sys import platform
import shutil
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
# Setup for web scrap. Need to Install different drivers for different OS
# https://pypi.org/project/selenium/

from selenium.webdriver.support.wait import WebDriverWait

#copy path to current folder
if platform == "linux" or platform == "linux2":
    driver_path = "./chromedriverLinux"
    # linux
elif platform == "darwin":
    driver_path = "./chromedriver"
    # OS X
elif platform == "win32":
    driver_path = "./chromedriver.exe"
    # Windows...
else:
    driver_path = "ERROR"

service = Service(executable_path=driver_path)
chrome_options = Options()

#find path of browser
chrome_options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

driver = webdriver.Chrome(service=service, options=chrome_options)

#Get to Indivdual Degree
def individualDegree(degree):
    # Starting website
    driver.get("https://catalog.ucsc.edu/Current/General-Catalog/Academic-Programs/Bachelors-Degrees")

    degreeLink = WebDriverWait(driver, 3).until(
        lambda d: d.find_element(By.LINK_TEXT, degree))
    degreeLink.click()

    reqLink = WebDriverWait(driver, 3).until(
        lambda d: d.find_element(By.CSS_SELECTOR, 'a[href*="degree-req-2"]'))
    reqLink.click()

    courseLinks = WebDriverWait(driver, 3).until(
        lambda d: d.find_elements(By.CSS_SELECTOR, "div#degree-req-2 div.expand div.expand table tbody a"))
    for i in courseLinks:
        i.click()

    time.sleep(8)

    course = WebDriverWait(driver, 300).until(
        lambda d: d.find_elements(By.CSS_SELECTOR, 'div[role*="dialog"] div#main h1 span:nth-child(2)'))

    subject = WebDriverWait(driver, 200).until(
        lambda d: d.find_elements(By.CSS_SELECTOR, 'div[role*="dialog"] div#main h1 span:nth-child(1)'))

    extraFields = WebDriverWait(driver, 1000).until(
        lambda d: d.find_elements(By.CLASS_NAME, "extraFields"))

    quarter = WebDriverWait(driver, 1000).until(
    lambda d: d.find_elements(By.CLASS_NAME, "quarter"))

    instructor = WebDriverWait(driver, 1000).until(
        lambda d: d.find_elements(By.CLASS_NAME, "instructor"))
    

    for i in course:
        print(i.text)

    for i in subject:
        print(i.text)

    for i in extraFields:
        print(i.text)

    for i in quarter:
        print(i.text)

    for i in instructor:
        print(i.text)

individualDegree('Agroecology B.A.')

degree = ['Agroecology B.A.',
'Anthropology B.A.',
'Applied Linguistics and Multilingualism B.A.',
'Applied Mathematics B.S.',
'Applied Physics B.S.',
'Art and Design: Games and Playable Media B.A.',
'Art B.A.',
'Biochemistry and Molecular Biology B.S.',
'Biology B.A.',
'Biology B.S.',
'Biomolecular Engineering and Bioinformatics B.S.',
'Biotechnology B.A.',
'Business Management Economics B.A.',
'Chemistry B.A.',
'Chemistry B.S.',
'Classical Studies B.A.',
'Cognitive Science B.S.',
'Community Studies B.A.',
'Computer Engineering B.S.',
'Computer Science B.A.',
'Computer Science B.S.',
'Computer Science: Computer Game Design B.S.',
'Critical Race and Ethnic Studies B.A.',
'Earth Sciences B.S.',
'Earth Sciences/Anthropology Combined Major B.A.',
'Ecology and Evolution B.S.',
'Economics B.A.',
'Economics/Mathematics Combined B.A.',
'Education, Democracy, and Justice B.A.',
'Electrical Engineering B.S.',
'Environmental Sciences B.S.',
'Environmental Studies B.A.',
'Environmental Studies/Biology Combined Major B.A.',
'Environmental Studies/Earth Sciences Combined Major B.A.',
'Environmental Studies/Economics Combined Major B.A.',
'Feminist Studies B.A.',
'Film and Digital Media B.A.',
'Global Economics B.A.',
'History B.A.',
'History of Art and Visual Culture B.A.',
'Human Biology B.S.',
'Jewish Studies B.A.',
'Language Studies B.A.',
'Latin American and Latino Studies B.A.',
'Latin American and Latino Studies/Politics Combined B.A.',
'Latin American and Latino Studies/Sociology Combined B.A.',
'Legal Studies B.A.',
'Linguistics B.A.',
'Literature B.A.',
'Marine Biology B.S.',
'Mathematics B.A.',
'Mathematics B.S.',
'Mathematics Education B.A.',
'Molecular, Cell, and Developmental Biology B.S.',
'Music B.A.',
'Music B.M.',
'Network and Digital Technology B.A.',
'Neuroscience B.S.',
'Philosophy B.A.',
'Physics (Astrophysics) B.S.',
'Physics B.S.',
'Plant Sciences B.S.',
'Politics B.A.',
'Psychology B.A.',
'Robotics Engineering B.S.',
'Science Education B.S.',
'Sociology B.A.',
'Spanish Studies B.A.',
'Technology and Information Management B.S.',
'Theater Arts B.A.']

driver.quit()
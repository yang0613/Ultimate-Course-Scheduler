from cgitb import text
from lib2to3.pgen2.driver import Driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sys import platform
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import shutil
import os

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

    main = WebDriverWait(driver, 200).until(
        lambda d: d.find_elements(By.CSS_SELECTOR, 'div[role*="dialog"] div#main'))

    courseID = WebDriverWait(driver, 200).until(
        lambda d: d.find_elements(By.CSS_SELECTOR, 'div[role*="dialog"] div#main h1 span:nth-child(2)'))

    courseName = WebDriverWait(driver, 200).until(
    lambda d: d.find_elements(By.CSS_SELECTOR, 'div[role*="dialog"] div#main'))

    subject = WebDriverWait(driver, 200).until(
        lambda d: d.find_elements(By.CSS_SELECTOR, 'div[role*="dialog"] div#main h1 span:nth-child(1)'))

    # prereq = WebDriverWait(driver, 200).until(
    #     lambda d: d.find_elements(By.XPATH, '//p[contains(text(), "Prerequisite")]'))

    # credit = WebDriverWait(driver, 200).until(
    #     lambda d: d.find_elements(By.CSS_SELECTOR, 'div[role*="dialog"] div#main div.extraFields p'))

    # quarter = WebDriverWait(driver, 200).until(
    # lambda d: d.find_elements(By.CLASS_NAME, "quarter"))

    # instructor = WebDriverWait(driver, 200).until(
    #     lambda d: d.find_elements(By.CLASS_NAME, "instructor"))

# data structure
    prereq = []
    className = []
    credit = []
    quarter = []
    instructor = []
    count = 0

    #className
    for i in range(len(courseName)):
        className.append(courseName[i].text.split('\n')[1].split('\n')[0])
    
    for i in range(len(main)):
        #prereq
        if 'Prerequisite(s): ' in main[i].text:
            prereq.append(main[i].text.split('Prerequisite(s): ')[1].split('\n')[0])
        else:
            prereq.append('')
        #credit
        credit.append(main[i].text.split('\nCredits ')[1].split('\n')[0])
        #quarter
        if '\nQuarter Offered ' in main[i].text:
            quarter.append(main[i].text.split('\nQuarter Offered ')[1].split('\n')[0])
        else:
            quarter.append('')
        #instructor
        if '\nInstructor ' in main[i].text:
            instructor.append(main[i].text.split('\nInstructor ')[1].split('\n')[0])
        else:
            instructor.append('')

# ('CSE 12', 'Computer Systems and Assembly Language and Lab', 'Computer Science and Engineering', 7, '["Fall","Winter","Spring","Summer"]', '["The Staff", "Tracy Larrabee", "Darrell Long", "Jose Renau Ardevol", "Matthew Guthaus", "Max Dunne", "Sagnik Nath"]')
# ('CSE 12', '["CSE 5J", "CSE 20","CSE 30","BME 160"]', '["Computer Science B.S."])    
    courseList = []
    reqList = []

    for i in range(0, len(courseID)):
        coursetuple = (courseID[i].text, className[i], subject[i].text, credit[i], quarter[i], instructor[i])
        courseList.append(coursetuple)
    # print(courseList)

        reqtuple = (courseID[i].text, prereq[i], degree)
        reqList.append(reqtuple)
    # print(reqList)

    return courseList, reqList
#edge case: 
# 'Anthropology B.A.', 'Earth Sciences B.S.', Environmental Studies B.A., 
# Film and Digital Media B.A., History B.A., 'History of Art and Visual Culture B.A.', 
# Mathematics B.A., Music B.A., Psychology B.A.
degree = [
'Agroecology B.A.',
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
'Theater Arts B.A.'
]



def dataToSQL(courses, reqs):
    # print(courses)
    # print(reqs)

    #rewrite
    # f = open('../database/data.sql', 'w')
    #append
    f = open('../database/data.sql', 'a')
    f.write("\n\nINSERT INTO Classes (classID, className, subject, credit, quarters, instructor) VALUES ")
    for i in courses:
        f.write("\n" + str(i) + ",")
    f.write("\nON CONFLICT (classID)\nDO NOTHING;\n")
    
    for i in reqs:
        f.write(" \nINSERT INTO Requirements VALUES ")
        f.write("\n" + str(i))
        f.write("\nON CONFLICT (classID) DO UPDATE SET gradReq = Requirements.gradReq || ', ' ||EXCLUDED.gradReq WHERE Requirements.gradReq NOT LIKE '%' || EXCLUDED.gradReq || '%';")
    f.close()


# courses, reqs = individualDegree('Agroecology B.A.')
# dataToSQL(courses, reqs)

for i in degree:
    courses, reqs = individualDegree(i)
    dataToSQL(courses, reqs)

driver.quit()
# dataToSQL()


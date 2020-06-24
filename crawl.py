from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import subprocess

subprocess.call(["sudo", "./Den-thesis/write_proc", "0.14285"])

time.sleep(2)

Options.binary_location = "/usr/bin/google-chrome"
webdriver_path = './chromedriver'
options = Options()
driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
driver.get("https://www.youtube.com/watch?v=rMGEMYaQiOg&feature=share&fbclid=IwAR1N4OGZ0xvSV9g5_rf__YgBVAwGwrJS1KDOjC4m9MuOaw4OEz3qWSLnC0A")

time.sleep(15)

portionSet = ["0.5", "0.44", "0.636", "1.5714", "2.2727", "2"] # Set of resource block changing portion.
portionInd = 0

preQuality = driver.find_elements_by_class_name("ytp-menu-label-secondary").text
preTime = time.time()
subprocess.call(["sudo", "./Den-thesis/write_proc", portionSet[portionInd]])
portionInd += 1

while True:
    curQuality = driver.find_elements_by_class_name("ytp-menu-label-secondary").text
    curTime = time.time()
    if curQuality != preQuality:
        if portionInd == len(portionSet): # Finish the quality testing.
            break

        qualityChangingInterval = curTime - preTime
        preTime = time.time()
        subprocess.call(["sudo", "./Den-thesis/write_proc", qualitySet[qualityInd]])
        portionInd += 1
        
driver.close()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import subprocess

subprocess.call(["sudo", "./Den-thesis/write_proc", "0.14285"])
print "Portion: 0.14285\n"

time.sleep(2)

Options.binary_location = "/usr/bin/google-chrome"
webdriver_path = './chromedriver'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
driver.get("https://www.youtube.com/watch?v=rMGEMYaQiOg&feature=share&fbclid=IwAR1N4OGZ0xvSV9g5_rf__YgBVAwGwrJS1KDOjC4m9MuOaw4OEz3qWSLnC0A")

time.sleep(15)

print "Start measuring.\n"
portionSet = ["0.5", "0.44", "0.636", "1.5714", "2.2727", "2"] # Set of resource block changing portion.
portionInd = 0

preQuality = driver.find_element_by_class_name("ytp-menu-label-secondary").text
preTime = time.time()
subprocess.call(["sudo", "./module/write_proc", portionSet[portionInd]])
print "Portion: " + portionSet[portionInd]
portionInd += 1

while True:
    try:
        curQuality = driver.find_element_by_class_name("ytp-menu-label-secondcary").text
    
    except StaleElementReferenceException as e:
        continue

    curTime = time.time()
    if curQuality != preQuality:
        if portionInd == len(portionSet): # Finish the quality testing.
            break

        preQuality = curQuality
        interval = curTime - preTime
        print "Changing interval: " + preQuality + "->" + curQuality + ":" + str(interval) + "\n"
        preTime = time.time()
        subprocess.call(["sudo", "./Den-thesis/write_proc", qualitySet[qualityInd]])
        print "Portion: " + portionSet[portionInd] + "\n"
        portionInd += 1
    time.sleep(5)
        
driver.close()

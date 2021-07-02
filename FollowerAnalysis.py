from Initialization import *
import selenium as sel
from scrape import *
import pandas as pd
def getFollowers(username):
    driver.get(f"https://www.instagram.com/{username}")
    driver.find_elements_by_class_name('-nal3 ')[1].click()
    usernames = []
    usernameElements = []
    startIndex = 0
    elsc = 0
    scrollDiv = driver.find_element_by_class_name('isgrP')
    lastUser = ""
    while True:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight;', scrollDiv)
        sleep(2)
        usernameElements = driver.find_elements_by_class_name('wo9IH')
        if usernameElements[-1].find_element_by_tag_name('a').get_attribute('href') == lastUser:
            break
        else:
            lastUser = usernameElements[-1].find_element_by_tag_name('a').get_attribute('href')

        print(len(usernameElements))
        elsc = elsc + len(usernameElements[startIndex:])
        print(elsc)


        usernameElements = usernameElements[startIndex:]
        for i in usernameElements:
            usernames.append(i.find_element_by_tag_name('a').get_attribute('href'))
        usernames = list(dict.fromkeys(usernames))
        print(len(usernames))
        if startIndex == 0:
            startIndex = len(usernameElements) - 1
        else:
            startIndex = startIndex + len(usernameElements)

    return usernames


driver = getFirefoxDriver()
driver.implicitly_wait(5)
userLinks = getFollowers()
usernames = []
dataDict = {
    'usernames':[],
    'avgLikes': [],
    'following':[]
}

for link in userLinks:
    data = instaScrape(link,driver)
    dataDict["usernames"].append(str(link).replace('www.instagram.com/', ''))
    dataDict["avgLikes"].append(data[0])
    dataDict["following"].append(data[1])

path = r'D:\CollectedData.xlsx'
writer = pd.ExcelWriter(path)
df = pd.DataFrame(dataDict)
df.to_excel(writer,"Data")
writer.save()






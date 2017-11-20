from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions
import time

pages = set()  # initialise Pages set
answers = set()

#get all urls questions posted on the page
#and get all anwsers for each question
def getLinks(pageUrl):
    global pages
    html = urlopen(pageUrl)
    bsObj = BeautifulSoup(html, "html.parser")

    try:
        for sibling in bsObj.findAll("div", {"class": "feed-main"}):
            page_url="https://www.zhihu.com"+sibling.find("a").attrs['href']
            pages.add(page_url)
    except AttributeError:
        print("This page is missing something! No worries though!")
    print(pages)

    for link in pages:
        getAllAns(link)

#get all posts under a question
def getAllAns(target_url):
    driver = webdriver.PhantomJS(executable_path="YOUR OWN PATH")
    clickSuccess = False
    while (not clickSuccess):
        driver.get(target_url)
        try:
            # get the amount of answers under a question
            for content in driver.find_elements_by_class_name("List-headerText"):
                print(content.text)
                for number in content.text.split():
                    if number.isdigit():
                        # decide how many "button click" operation should be done
                        if int(number)<=20:
                            number_of_iteration=-1
                            clickSuccess=True
                        else:
                            number_of_iteration = int(number) / 20
                        print(number_of_iteration)
        except exceptions.WebDriverException:
            print("A exception has occured!")

        time.sleep(0.5)
        # click the button on the page to get all answers displayed on the page
        for i in range(0, int(number_of_iteration) + 1):
            try:
                driver.find_element_by_css_selector(".Button.QuestionMainAction").click()
                clickSuccess = True
                time.sleep(1)
            except exceptions.ElementNotVisibleException:
                print("ElementNotVisibleException")
            except exceptions.NoSuchElementException:
                print("NoSuchElementException")
            except exceptions.InvalidSelectorException:
                print("InvalidSelectorException")

    try:
        for content in driver.find_elements_by_class_name("List-item"):
            with open('Zhihu_ADR.txt', 'a', encoding="utf-8") as f:
                content_str = content.text + "\n"+\
                              "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
                f.write(content_str)
                print(content.text)
    except exceptions.WebDriverException:
        print("A exception has occured!")

    finally:
        driver.close()

#Enter point
getLinks("Target url of a Topic")

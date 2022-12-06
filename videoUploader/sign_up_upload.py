from dependency.selenium.Selenium import getSeleniumBrowserAutomation
from time import sleep
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from string import ascii_letters
import random
from dependency.faker.Faker import getFakerInstance
from dependency.database.index import getDatabaseWrapperInstance

def getRandomString(length):
    return ''.join(random.choice(ascii_letters+"1234567890") for i in range(length))

def getRandomEmail():
    faker=getFakerInstance()
    name=faker.name()
    name=name.replace(" ","")
    random_string=getRandomString(5)
    return f"{name}{random_string}@gmail.com"

def getRandomPassword():
    return getRandomString(10)    

    
def get_random_user_cred():
    email=getRandomEmail()
    username=email.split("@")[0]
    return [username,email,getRandomPassword()]

def upload(browser,url,video_url,title):
    try:
        browser.get(f"{url}/users/upload")
        browser.execute_script('upload_show_url()')
        sleep(4)
        browser.find_element(By.CSS_SELECTOR,".url_upload input").send_keys(video_url)
        sleep(2)
        browser.execute_script('resumable_check_url()')
        
        sleep(4)

        browser.find_element(By.CSS_SELECTOR,"#name_inp").send_keys(title)
        browser.execute_script(''' 
            document.querySelector(".radio-boxes-orientation");
            document.querySelector(".radio-boxes-orientation label").click();
            ''')

        tags=browser.execute_script('''
                return document.querySelector("#category_list").innerText;
            ''')

        tags=tags.split("\n")
        for t in random.choices(tags,k=2):
            element=browser.find_element(By.CSS_SELECTOR,"#tag_inp input")
            element.send_keys(t)
            element.send_keys(Keys.ENTER)
        browser.execute_script('''items=document.querySelectorAll("#category_list label");for(var item of items){item.click()};''')
        browser.execute_script('''document.querySelector("#upload_form_button").click()''')

    except Exception as e:
        print(e)



def sign_up(video_url,title):
    print(video_url,title)
    url="https://spankbang.com"
    browser=getSeleniumBrowserAutomation()
    browser.get(url)
    
    browser.find_element(By.CLASS_NAME,"bt_signup").click()
    [username,email,password]=get_random_user_cred()
    print(username,email,password)
    sleep(2)

    browser.find_element(By.ID,"reg_username").send_keys(username)
    browser.find_element(By.ID,"reg_password").send_keys(password)
    browser.find_element(By.ID,"reg_email").send_keys(email)

    browser.find_element(By.CLASS_NAME,"btn").click()
    sleep(2)
    upload(browser,url,video_url,title)

    db=getDatabaseWrapperInstance(table_name="spankbang_account")
    db.insert(collection="accounts",data={
        "username":username,
        "email":email,
        "password":password,
        "video":video_url
    })


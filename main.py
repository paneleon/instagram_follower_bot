import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from time import sleep

CHROME_DRIVER_PATH = "C:/Development/chromedriver.exe"
INSTAGRAM_LINK = "https://www.instagram.com/"
SIMILAR_ACCOUNT = "meetup"

USERNAME = os.environ.get("INST_USERNAME")
PASSWORD = os.environ.get("INST_PASSWORD")

print(USERNAME)
print(PASSWORD)


class InstaFollower:

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.base_window = self.driver.window_handles[0]

    def login(self):
        self.driver.get(INSTAGRAM_LINK)
        sleep(2)
        username = self.driver.find_element_by_name("username")
        username.send_keys(USERNAME)
        password = self.driver.find_element_by_name("password")
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)
        sleep(2)

        self.close_popups()

    def close_popups(self):
        # save information?
        try:
            sleep(5)
            dont_save_button = self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div/div/button')
            dont_save_button.click()
            sleep(2)
        except NoSuchElementException:
            print("Prompt was already handled")
            pass
        # turn on notifications?
        try:
            sleep(5)
            turn_off_button = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]')
            turn_off_button.click()
            sleep(2)
        except NoSuchElementException:
            print("Prompt was already handled")
            pass

    def find_followers(self):
        # self.driver.get(f"{INSTAGRAM_LINK}/{SIMILAR_ACCOUNT}/")
        try:
            search_box = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
            sleep(2)
            search_box.send_keys(SIMILAR_ACCOUNT)
            search_box.send_keys(Keys.ENTER)
            sleep(2)
            account_found = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a')
            account_found.click()
        except ElementClickInterceptedException:
            self.close_popups()

        sleep(5)
        followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        followers.click()
        sleep(2)

        followers_window = self.driver.find_element_by_css_selector('.isgrP')
        for i in range(30):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_window)
            sleep(2)

        # this kinda worked
        # followers_window = self.driver.find_element_by_xpath("//div[@Class='isgrP']//a")
        # followers_window.send_keys(Keys.END)

    def follow(self):
        follow_buttons = self.driver.find_elements_by_css_selector("button.sqdOP")
        print(len(follow_buttons))
        for button in follow_buttons:
            if button.text.lower() == "follow":
                try:
                    button.click()
                    sleep(1)
                except ElementClickInterceptedException:
                    # <button class="aOOlW   HoLwm " tabindex="0">Cancel</button>
                    cancel_button = self.driver.find_element_by_css_selector("button.aOOlW.HoLwm")
                    cancel_button.click()
                    sleep(3)

    def unfollow(self):
        follow_buttons = self.driver.find_elements_by_css_selector("button.sqdOP")
        for button in follow_buttons:
            if button.text.lower() == "following" or button.text.lower() == "requested":
                button.click()
                sleep(1)
                unfollow_button = self.driver.find_element_by_css_selector("button.aOOlW")
                unfollow_button.click()
                sleep(3)


follower_bot = InstaFollower()
follower_bot.login()
follower_bot.find_followers()
follower_bot.follow()
# follower_bot.unfollow()

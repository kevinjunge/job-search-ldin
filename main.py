from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
class JobApply:

    def __init__(self, data):
        """Parameter initialization"""
        
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver = webdriver.Chrome(data['driver_path'])

    def login_linkedin(self):
        """This function logs into linkedin"""

        # make driver go to the linkedin login url
        self.driver.get("https://www.linkedin.com/login/")
        
        # introduce email and password and hit enter
        login_email = self.driver.find_element_by_name("session_key")
        # clear() -> clean the text and enable it
        login_email.clear()
        login_email.send_keys(self.email)
        login_password = self.driver.find_element_by_name("session_password")
        login_password.clear()
        login_password.send_keys(self.password)
        login_password.send_keys(Keys.RETURN)

    def job_search(self):
        # this function goes to the 'Jobs' section and looks for all the jobs that
        # matches the keywords and location
        # 
        # go to jobs section:
        jobs_link = self.driver.find_element_by_link_text('Jobs')
        jobs_link.click()
        time.sleep(2)

        # introduce our keyword and location and hit enter
        search_keyword = self.driver.find_element_by_xpath("//input[starts-with(@id, 'jobs-search-box-keyword')]")
        search_keyword.clear()
        search_keyword.send_keys(self.keywords)
        time.sleep(2)
        search_location = self.driver.find_element_by_xpath("//input[starts-with(@id, 'jobs-search-box-location')]")
        search_location.clear()
        search_location.send_keys(self.location)
        time.sleep(1)
        search_keyword.send_keys(Keys.RETURN)

    def filter(self):
        """This function filters all the job results"""

        # select all filters, click on easy apply and apply the filter
        all_filters_button = self.driver.find_element_by_xpath("//button[starts-with(@aria-label, 'Show all filters')]")
        all_filters_button.click()
        time.sleep(1)
        easy_apply_button = self.driver.find_element_by_xpath("//div[@class='jobs-search-advanced-filters__binary-toggle']")
        easy_apply_button.click()
        time.sleep(1)
        apply_filters_button = self.driver.find_element_by_xpath("//button[starts-with(@aria-label, 'Apply current filters')]")
        apply_filters_button.click()
        time.sleep(1)

if __name__ == "__main__":
    
    with open('config.json') as config_file:
        data = json.load(config_file)


    bot = JobApply(data)
    bot.login_linkedin()
    time.sleep(2)
    bot.job_search()
    time.sleep(2)
    bot.filter()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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

    def find_offers(self):
        """This function finds all the offers through all the pages result of the search and filtering"""

        # find the total amount of results (in case there are more than 24 of them)
        total_results = self.driver.find_element_by_class_name("jobs-search-results-list__text.display-flex.t-12.t-black--light.t-normal")
        total_results_int = int(total_results.text.split(' ', 1)[0].replace(',',''))
        print(total_results_int)
        
        time.sleep(2)
        # get results of first page
        current_page = self.driver.current_url
        results = self.driver.find_elements_by_class_name("jobs-search-results__list-item.occludable-update.p0.relative.ember-view")

        # for each job add, submits and application if no questions are asked
        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()






    def submit_application(self, job_ad):
        """This function submits the application for the job ad found"""
        
        print("You are applying to the positon of: ", job_ad.text)
        job_ad.click()
        time.sleep(2)

        # click on the easy apply button, skip if already applied to the position
        try:
            in_apply = self.driver.find_element_by_class_name("jobs-apply-button.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view")
            in_apply.click()
            print("--->Clicked on easy apply")
        except:
            print("You already applied to this job, go to next job...")
            pass
        time.sleep(1)

        # try to submit application if the application is available
        try:
            submit = self.driver.find_element_by_xpath("//button[starts-with(@aria-label, 'Submit application')]")
            submit.send_keys[Keys.RETURN]
            print("--->Clicked on submit")
            time.sleep(1)
        # .. if button is not available, discard application and go to next one
        except NoSuchElementException:
            print("Not direct application, going to next...")
            try:
                discard = self.driver.find_element_by_xpath("//button[@data-test-modal-close-btn]")
                discard.send_keys(Keys.RETURN)
                time.sleep(1)
                discard_confirm = self.driver.find_element_by_xpath("//button[@data-control-name='discard_application_confirm_btn']")
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(1)
            except NoSuchElementException:
                pass

if __name__ == "__main__":
    
    with open('config.json') as config_file:
        data = json.load(config_file)


    bot = JobApply(data)
    bot.login_linkedin()
    time.sleep(2)
    bot.job_search()
    time.sleep(2)
    bot.filter()
    time.sleep(1)
    bot.find_offers()
    time.sleep(1)
    

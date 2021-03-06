from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import re

class ApplyJob:

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
        
        # add in the email
        # (note: at config file: make sure to put in right email value for 'email' key)
        login_email = self.driver.find_element_by_name("session_key")
        # clear() -> clean the text and enable it
        login_email.clear()
        login_email.send_keys(self.email)
        # add in password 
        # (note: at config file: make sure to put in right password value for 'password' key)
        login_password = self.driver.find_element_by_name("session_password")
        login_password.clear()
        login_password.send_keys(self.password)
        # Hit Enter to login with credentials provided
        login_password.send_keys(Keys.RETURN)

    def job_search(self):
        """ this function goes to the 'Jobs' section and looks for all the jobs that
            matches the keywords and location.
        """
        # go to jobs section:
        jobs_link = self.driver.find_element_by_link_text('Jobs')
        jobs_link.click()
        time.sleep(2)
        # enter keyword(s) on job search
        search_keyword = self.driver.find_element_by_xpath("//input[starts-with(@id, 'jobs-search-box-keyword')]")
        search_keyword.clear()
        search_keyword.send_keys(self.keywords)
        time.sleep(2)
        # enter location on location search
        search_location = self.driver.find_element_by_xpath("//input[starts-with(@id, 'jobs-search-box-location')]")
        search_location.clear()
        search_location.send_keys(self.location)
        time.sleep(2)
        # return job results
        search_keyword.send_keys(Keys.RETURN)

    def filter(self):
        """This function filters all the job results based on filters applied"""

        # select all filters, click on easy apply and apply the filter
        self.apply_xpath_button("//button[starts-with(@aria-label, 'Show all filters')]")

        # sort by most recent
        self.apply_xpath_button("//label[@for='advanced-filter-sortBy-DD']")

        # filters on jobs added in last 24 hrs
        self.apply_xpath_button("//label[@for='advanced-filter-timePostedRange-r86400']")

        # filters on entry level jobs
        self.apply_xpath_button("//label[@for='advanced-filter-experience-2']")

        # filters on jobs that has easy apply
        self.apply_xpath_button("//div[@class='jobs-search-advanced-filters__binary-toggle']")

        # filters on jobs in information technology
        self.apply_xpath_button("//label[@for='advanced-filter-function-it']")

        # filters on jobs added in engineering
        self.apply_xpath_button("//label[@for='advanced-filter-function-eng']")

        # click 'Show results'
        self.apply_xpath_button("//button[starts-with(@aria-label, 'Apply current filters')]")

    def apply_xpath_button(self, xpath_str):
        try:
            # filters on jobs in information technology
            element_button = self.driver.find_element_by_xpath(xpath_str)
            element_button.click()
            time.sleep(1)
        except NoSuchElementException:
            pass

    def find_offers(self):
        """This function finds all the offers through all the pages result of the search and filtering"""

        # find the total amount of results (in case there are more than 24 of them)
        total_results = self.driver.find_element_by_class_name("jobs-search-results-list__text.display-flex.t-12.t-black--light.t-normal")
        total_results_int = int(total_results.text.split(' ', 1)[0].replace(',',''))
        print(total_results_int)
        
        # time.sleep(2)
        # get results of first page
        current_page = self.driver.current_url
        self.return_results()

        # if there's more than one page, find the pages and apply to the results of each page
        if total_results_int > 24:
            time.sleep(2)

            # find the last page and construct url of each page based on total amount of pages
            find_pages = self.driver.find_elements_by_class_name("artdeco-pagination__indicator.artdeco-pagination__indicator--number.ember-view")
            total_pages = find_pages[len(find_pages)-1].text
            total_pages_int = int(re.sub(r"[^\d.]","",total_pages))
            get_last_page = self.driver.find_element_by_xpath("//button[@aria-label='Page "+ str(total_pages_int)+"']")
            get_last_page.send_keys(Keys.RETURN)
            time.sleep(2)
            last_page = self.driver.current_url
            total_jobs = int(last_page.split('start=',1)[1])
  
            # go through all available pages and job offers and apply
            for page_number in range(25,total_jobs+25,25):
                self.driver.get(current_page+"&start="+str(page_number))
                self.return_results()
        else:
            self.end_session()

    def return_results(self):
        """ this function goes through each job in page and apply"""
        time.sleep(2)
        results = self.driver.find_elements_by_class_name("jobs-search-results__list-item.occludable-update.p0.relative.ember-view")
        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            titles = result.find_elements_by_class_name("disabled.ember-view.job-card-container__link.job-card-list__title")
            for title in titles:
                d = ['software', 'data', 'QA', 'engineer', 'python', 'java', 'sql', 'database','scala', 'c#', 'developer', 'etl']
                s = title.text.split(' ')
                found_match = False
                for i in s:
                    if i.lower() in d:
                        found_match = True
                        break
                if found_match:
                    self.submit_application(title)        

    def submit_application(self, job_link):
        """This function submits the application for the job ad found"""

       # job_link = WebDriverWait(driver, 5000).until(EC.visibility_of_element_located(
        #    (By.XPATH, "")
       # ))

        job_link.click()
        time.sleep(2)

        # click on the easy apply button, skip if already applied to the position
        try:
            in_apply = self.driver.find_element_by_class_name("jobs-apply-button.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view")
            in_apply.click()
            time.sleep(1)
            self.apply_job(job_link)
        except:
            # print("You already applied to this job, go to next job...")
            pass

    def apply_job(self, job_link):
        # try to submit application if the application is available
        self.submit_session()
        time.sleep(1)
        self.close_session(job_link)
        time.sleep(1)
        self.driver.find_element_by_class_name

    def submit_session(self):
        counter = 0
        while(True or counter > 7):
            if counter > 7:
                break
            try:
                next_button = self.driver.find_element_by_class_name("artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view")
                next_button.click()
                time.sleep(1)
            except NoSuchElementException:
                break
            counter +=1

    def close_session(self, job_link):
        # close it
        try:
            close_button = self.driver.find_element_by_class_name("artdeco-modal__dismiss.artdeco-button.artdeco-button--circle.artdeco-button--muted.artdeco-button--2.artdeco-button--tertiary.ember-view")
            close_button.click()
            time.sleep(1)
            try:
                # save applications that couldn't be applied
                save_confirm = self.driver.find_element_by_class_name("artdeco-modal__confirm-dialog-btn.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view")
                save_confirm.click()
                time.sleep(1)
                print("--->Need to apply: " + job_link.text)
            except NoSuchElementException:
                print("--->Clicked on submit: " + job_link.text)
        except NoSuchElementException:
            pass
    
    def end_session(self):
        """This function ends the actual session"""
        
        # print('End of the session, see you later!')
        self.driver.close()

    def apply(self):
        """Apply to job offers"""
        
        self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(5)
        self.job_search()
        time.sleep(5)
        self.filter()
        time.sleep(2)
        self.find_offers()
        time.sleep(2)



if __name__ == "__main__":
    
    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = ApplyJob(data)
    bot.apply()
    

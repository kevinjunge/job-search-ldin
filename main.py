from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json

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




if __name__ == "__main__":
    
    with open('config.json') as config_file:
        data = json.load(config_file)


    bot = JobApply(data)
    bot.login_linkedin()

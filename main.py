from selenium import webdriver
import json

class JobApply:

    def __init__(self, data):
        """Parameter initialization"""
        
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver_path = webdriver.Chrome(data['driver_path'])


if __name__ == "__main__":
    
    with open('config.json') as config_file:
        data = json.load(config_file)


    bot = JobApply(data)


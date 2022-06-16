automate job search - linkedin
Tech stack: Python, jSon, Selenium, Chrome driver
•	Logs into linkedin based on credentials saved up in .json file
•	Goes to job section and applies keyword(s) and location on the search bar(s)
•	On the job results it applies the necessary filters that’s been programmed to do
•	For each job link, it clicks, goes to all pages of job link and submits application. If unable to resolve some of questions, the job link is saved up for user to manually apply if necessary.
•	Goes through all the pages of job posts, and once complete, closes window and prints total number of jobs found, which jobs were applied, and which jobs were saved up.

Note:
 - makes sure chromedriver downloaded corresponds to google chrome version 

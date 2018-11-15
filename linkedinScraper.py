import time
from datetime import datetime 

import requests
from selenium import webdriver


class LinkedinScraper:
    """
    Scrapes the job postings from the Linkedin job board
    """

    def __init__(self):
        self.driver = webdriver.Chrome()

    def search(self, keywords, location, start):
        def build_link():
            link = 'https://www.linkedin.com/jobs/search/?'
            link += 'keywords={}'.format('%20'.join(keywords.split()))
            link += '&location={}'.format('%20'.join(location.split()))
            link += '&start={}'.format(start)
            link += '&trk=jobs_jserp_posted_one_day'
            return link

        self.keywords = keywords
        self.location = location

        link = build_link()
        self.driver.get(link)

    def login(self, user, pw):
        login_page_link = self.driver.get('https://www.linkedin.com/uas/login')
        self.driver.find_element_by_css_selector('input#username').send_keys(user)
        self.driver.find_element_by_css_selector('input#password').send_keys(pw)
        self.driver.find_element_by_css_selector('button').click()


    def scrape_jobs(self):
        job_postings = []
        for elem in self.driver.find_elements_by_css_selector('li'):
            if 'ember' in elem.get_attribute('id') and 'occludable-update' in elem.get_attribute('class'):
                job_postings.append(elem)

        job_data = []

        for elem in job_postings:
            elem.click()
            print('sleeping; waiting for job posting to load...')
            time.sleep(1)
            buttons = self.driver.find_elements_by_css_selector('button')

            job_information = {
                    'title': '',
                    'description': '',
                    'link': '',
                    'date': datetime.now().date(),
                    'keywords': self.keywords,
                    'location': self.location
            }

            # get title
            for h1 in self.driver.find_elements_by_css_selector('h1'):
                if 'jobs-details-top-card__job-title' in h1.get_attribute('class'):
                    job_information['title'] = h1.text

            # get article description
            for div in self.driver.find_elements_by_css_selector('div'):
                if 'jobs-box__html-content' in div.get_attribute('class'):
                    job_information['descripton'] = div.text

            for button in buttons:
                if 'ember' in button.get_attribute('id') and 'jobs-apply-button' in button.get_attribute('class'):
                    if 'Easy Apply' in button.text:
                        # have to implement easy apply handler
                        break
                    print(button.get_attribute('id'), button.get_attribute('class'))
                    button.click()
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    time.sleep(3)
                    print('sleeping; waiting for page to load...')
                    job_information['link'] = self.driver.current_url
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    break
            job_data.append(job_information)

        return job_data 


#scraper = LinkedinScraper()
#scraper.login(input('Username?'), input('Password?'))
#scraper.search('software intern', 'San Francisco Bay Area', 0)
#scraper.scrape_jobs()

import time
from datetime import datetime 

import requests
from selenium import webdriver, common


class LinkedinScraper:
    """
    Scrapes the job postings from the Linkedin job board
    """

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(10)
        self.logged_in = False

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
        time.sleep(2)

    def login(self, user, pw):
        login_page_link = self.driver.get('https://www.linkedin.com/uas/login')
        self.driver.find_element_by_css_selector('input#username').send_keys(user)
        self.driver.find_element_by_css_selector('input#password').send_keys(pw)
        self.driver.find_element_by_css_selector('button').click()
        self.logged_in = True


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
                try:
                    if 'jobs-box__html-content' in div.get_attribute('class'):
                        job_information['descripton'] = div.text
                except common.exceptions.StaleElementReferenceException:
                    print('stale element; ignoring and continuing...')


            for button in buttons:
                if 'ember' in button.get_attribute('id') and 'jobs-apply-button' in button.get_attribute('class'):
                    if 'Easy Apply' in button.text:
                        # have to implement easy apply handler
                        break
                    button.click()
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    time.sleep(3)
                    print('sleeping; waiting for page to load...')
                    try:
                        job_information['link'] = self.driver.current_url
                    except common.exceptions.TimeoutException:
                        print('timed out; moving on...')
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    break
            job_data.append(job_information)

        return job_data 

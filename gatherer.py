import os
from datetime import datetime

import pandas as pd

class Gatherer:
    """
    Gathers and stores the job applications that scrapers scrape off the job boards.
    """

    def __init__(self, scraper):
        self.scraper = scraper
        self.current_scrape = []

    def ingest_data(self, job_data):
        self.current_scrape += job_data
        pass

    def gather_jobs(self, keywords, location):
        start = 0
        if not self.scraper.logged_in:
            user = input('Username?')
            pw = input('Password?')
            self.scraper.login(user, pw)

        self.scraper.search(keywords, location, start)
        print('scraping jobs at {}...'.format(start))
        job_data = self.scraper.scrape_jobs()
        self.ingest_data(job_data)
        job_data_per_pagination = len(job_data)
        start += job_data_per_pagination

        while len(job_data) == job_data_per_pagination:
            self.scraper.search(keywords, location, start)
            print('scraping jobs at {}...'.format(start))
            job_data = self.scraper.scrape_jobs()
            start += job_data_per_pagination
            self.ingest_data(job_data)

    def digest_data(self):
        print('digesting scraped data...')
        application_types = {
            'taleo': [],
            'myworkday': [],
            'lever': [],
            'treehouse': [],
            'other': []
        }
        for job in self.current_scrape:
            discovered_type = False
            for application_type in application_types:
                if application_type in job['link']:
                    application_types[application_type].append(job)
                    discovered_type = True
            if not discovered_type:
                application_types['other'].append(job)

        os.chdir('job_data')
        try:
            os.chdir(self.scraper.keywords+'_'+self.scraper.location)
        except OSError:
            os.mkdir(self.scraper.keywords+'_'+self.scraper.location)
            os.chdir(self.scraper.keywords+'_'+self.scraper.location)

        for application_type in application_types:
            try:
                os.chdir(application_type)
            except OSError:
                os.mkdir(application_type)
                os.chdir(application_type)
            pd.DataFrame(application_types[application_type]).to_csv(str(datetime.now().date()), index=False)
            os.chdir('..')


if __name__ == "__main__":
    from linkedinScraper import LinkedinScraper

    scraper = LinkedinScraper()
    gatherer = Gatherer(scraper)
    gatherer.gather_jobs('software intern python', 'New York')
    gatherer.digest_data()

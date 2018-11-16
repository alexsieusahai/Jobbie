import os
from datetime import datetime

import pyodbc

class Gatherer:
    """
    Gathers and stores the job applications that scrapers scrape off the job boards.
    """

    def __init__(self, scraper):
        self.scraper = scraper
        self.current_scrape = []
        self.jobbie_user = os.environ['JOBBIE_USER']
        self.jobbie_pw = os.environ['JOBBIE_PW']

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
        if job_data_per_pagination == 0:
            return 
        start += job_data_per_pagination

        while len(job_data) == job_data_per_pagination:
            self.scraper.search(keywords, location, start)
            print('scraping jobs at {}...'.format(start))
            job_data = self.scraper.scrape_jobs()
            start += job_data_per_pagination
            self.ingest_data(job_data)

    def digest_data(self):
        cnxn_str = "DRIVER={MySQL ODBC 8.0 Driver};SERVER=jobbie-db.cpggzb24ffm6.ca-central-1.rds.amazonaws.com;DATABASE=jobbie_db;"
        cnxn_str += 'UID='+self.jobbie_user+';'
        cnxn_str += 'PASSWORD='+self.jobbie_pw+';'
        cursor = pyodbc.connect(cnxn_str).cursor()

        columns = ['title', 'description', 'link', 'date', 'keywords', 'location']
        sql_stem = 'INSERT INTO jobPostings('
        sql_stem += ', '.join(columns) + ')\nVALUES\n'
        for job in self.current_scrape:
            sql = sql_stem + '('
            sql += ', '.join(['"'+str(job[col]).replace('"', '')+'"' for col in columns]) + ')'
            try:
                cursor.execute(sql)
                cursor.commit()
            except pyodbc.IntegrityError:
                print('already scraped this one before; rolling back and moving on...')
                cursor.rollback()

        self.current_scrape = []


if __name__ == "__main__":
    from linkedinScraper import LinkedinScraper
    scraper = LinkedinScraper()
    gatherer = Gatherer(scraper)
    gatherer.gather_jobs('software intern python', 'New York')
    gatherer.digest_data()

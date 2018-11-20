import sys
import os
from datetime import datetime

import pyodbc

sys.path.append('..')
from cursor_wrapper import get_cursor

class Gatherer:
    """
    Gathers and stores the job applications that scrapers scrape off the job boards.
    """

    def __init__(self, scraper):
        self.scraper = scraper
        self.current_scrape = []
        self.jobbie_user = os.environ['JOBBIE_USER']
        self.jobbie_pw = os.environ['JOBBIE_PW']


    def gather_jobs(self, keywords, location, start=0, progress_file=None):
        if not self.scraper.logged_in:
            user = os.environ['LINKEDIN_USER']
            pw = os.environ['LINKEDIN_PW']
            self.scraper.login(user, pw)

        self.scraper.search(keywords, location, start)
        print('scraping jobs at {}...'.format(start))
        job_data = self.scraper.scrape_jobs()
        self.digest_data(job_data)
        if progress_file:
            self.save_progress(progress_file, start)

        job_data_per_pagination = len(job_data)
        if job_data_per_pagination == 0:
            return 
        start += job_data_per_pagination

        while len(job_data) == job_data_per_pagination:
            self.scraper.search(keywords, location, start)
            print('scraping jobs at {}...'.format(start))
            job_data = self.scraper.scrape_jobs()
            start += job_data_per_pagination
            self.digest_data(job_data)
            if progress_file:
                self.save_progress(progress_file, start)


    def digest_data(self, job_data):
        cursor = get_cursor()

        columns = ['title', 'description', 'link', 'date', 'keywords', 'location', 'company']
        sql_stem = 'INSERT INTO jobPostings('
        sql_stem += ', '.join(columns) + ')\nVALUES\n'
        for job in job_data:
            sql = sql_stem + '('
            sql += ', '.join(['"'+str(job[col]).replace('"', '')+'"' for col in columns]) + ')'
            try:
                cursor.execute(sql)
                cursor.commit()
            except pyodbc.IntegrityError:
                print('already scraped this one before; rolling back and moving on...')
                cursor.rollback()


    def save_progress(self, progress_file, start):
        f = open(progress_file, 'w')
        f.write(str(start))
        f.close()


if __name__ == "__main__":
    from linkedinScraper import LinkedinScraper
    scraper = LinkedinScraper()
    gatherer = Gatherer(scraper)
    gatherer.gather_jobs('software intern python', 'New York')

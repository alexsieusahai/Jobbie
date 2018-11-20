import os
import sys

sys.path.append('..')

from linkedinScraper import LinkedinScraper
from gatherer import Gatherer
from watchdog import Watchdog

def scrape():
    scraper = LinkedinScraper()
    scraper.login(os.environ['LINKEDIN_USER'], os.environ['LINKEDIN_PW'])
    gatherer = Gatherer(scraper)
    watchdog = Watchdog(gatherer)

    job_list = [
            'data intern',
            'machine learning intern', 
            'software intern',
            'python intern'
            ]

    location_list = [
            'Vancouver',
            'New York',
            'San Francisco Bay Area',
            'Toronto',
            ]

    for job in job_list:
        for location in location_list:
            print('gathering for', job, location)
            watchdog.monitor_gather(job, location)

    for job in job_list:
        print('gathering for', job, 'Worldwide')
        watchdog.monitor_gather(job, 'Worldwide')

    return 'Done'

if __name__ == "__main__":
    scrape()

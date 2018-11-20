import os

from linkedinScraper import LinkedinScraper
from gatherer import Gatherer

from flask import Flask
app = Flask(__name__)

@app.route('/scrape')
def scrape():
    scraper = LinkedinScraper()
    scraper.login(os.environ['LINKEDIN_USER'], os.environ['LINKEDIN_PW'])
    gatherer = Gatherer(scraper)

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
            'Toronto'
            ]

    search_list = []
    for job in job_list:
        for location in location_list:
            print('gathering for', job, location)
            gatherer.gather_jobs(job, location)
            gatherer.digest_data()

if __name__ == "__main__":
    #app.run(host="0.0.0.0", debug=True)
    scrape()

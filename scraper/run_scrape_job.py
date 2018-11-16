from linkedinScraper import LinkedinScraper
from gatherer import Gatherer

scraper = LinkedinScraper()
scraper.login(input('Username?'), input('Password?'))
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

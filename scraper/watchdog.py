class Watchdog:
    """
    Watches and revives the scrape whenever it dies.
    """
    def __init__(self, gatherer):
        self.gatherer = gatherer

    def monitor_gather(self, keywords, location, start=0):
        while True:
            #try:
            self.gatherer.gather_jobs(keywords, location, start, progress_file='progress')
            break
            #except Exception as e:
            #    print('ERROR!')
            #    print(e)
            #    print('********************************')
            #    start = int(open('progress').read())


if __name__ == "__main__":
    import os

    from gatherer import Gatherer
    from linkedinScraper import LinkedinScraper

    scraper = LinkedinScraper()
    #scraper.login(os.environ['LINKEDIN_USER'], os.environ['LINKEDIN_PW'])
    gatherer = Gatherer(scraper)
    watchdog = Watchdog(gatherer)

    keywords = 'software intern'
    location = 'Worldwide'

    watchdog.monitor_gather(keywords, location)

import sys
sys.path.append('..')

from cursor_wrapper import get_cursor

class JobGetter:
    """
    Handles the getting process.
    """
    def __init__(self, days_behind=None):
        self.days_behind = days_behind

    def get_job_list(self):
        cursor = get_cursor()
        sql = 'SELECT * FROM jobPostings '         
        if self.days_behind:
            sql += 'WHERE DATEDIFF(CURDATE(), date) <= {}'.format(days_behind)
        obj = cursor.execute(sql)
        self.jobs = obj.fetchall()
        return self.jobs

    def filter_jobs_by_applier_type(self, applier_type):
        applicable_jobs = []
        for job in self.jobs:
            if applier_type in job.link:
                applicable_jobs.append(job)

        return applicable_jobs


if __name__ == "__main__":
    from user import User

    jg = JobGetter()
    jg.get_job_list()

    greenhouse_jobs = jg.filter_jobs_by_applier_type('greenhouse')
    for job in greenhouse_jobs:
        print(job)

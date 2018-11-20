from jobGetter import JobGetter

jg = JobGetter()
jg.get_job_list()

for applier_type in ['greenhouse', 'lever']:
    for job in jg.filter_jobs_by_applier_type(applier_type):
        print('****************************************')
        print(job[0])
        print(job.description)
        print(job.link)
        input('Press enter when you have finished with this job.')

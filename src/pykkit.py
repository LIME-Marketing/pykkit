import argparse
import json
from subprocess import call
import time
import atexit

class Pykkit:
    def __init__(self, files):
        self.files = files
        self.jobs_run = 0
        self.jobs = []

    def execute(self):
        def job_timer():
            print "{} jobs completed in {} seconds".format(self.jobs_run, time.time() - self.start_time)
        def process_file(job_file):
            data = json.load(job_file)
            if 'includes' in data:
                for filename in data['includes']:
                    include_file = open(filename)
                    process_file(include_file)
            if 'jobs' in data:
                self.jobs.extend(data['jobs'])
        def run_job(job):
            print "----- JOB #{} -----".format(self.jobs_run + 1)
            print "Description:", job.get('description', 'None given')
            exit_code = call(job['command'], shell=job.get('shell', False))
            print "SUCCESS" if exit_code == 0 else "FAIL (job exited with code {})".format(exit_code), "\n"

        atexit.register(job_timer)

        self.start_time = time.time()
        for job_file in self.files:
            process_file(job_file)
        for job in self.jobs:
            run_job(job)
            self.jobs_run += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute the pykkit job queue')
    parser.add_argument('files', type=file, nargs='+')

    args = parser.parse_args()

    pykkit = Pykkit(args.files)
    pykkit.execute()

import os
import argparse
import json
from google.cloud import batch_v1
from file_processing import process_jobs 
from batch import create_job_request
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
                        prog='Cloud batch launder',
                        description='Launches Cloud Batch jobs in /jobs directory')   
    parser.add_argument('-p', '--project_id', default='climateiq')
    parser.add_argument('-r', '--region_id', default='us-central1')
    parser.add_argument('--dry_run', action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    print(f"Program arguments {args}")

    batch_directory = os.path.dirname(os.path.dirname(__file__))
    jobs_directory = os.path.join(batch_directory, "jobs")
    jobs = process_jobs(jobs_directory)
    client = batch_v1.BatchServiceClient()

    for jobname, job in jobs.items():
        request = create_job_request(args.project_id, args.region_id, jobname, job)

        print(f"Job Name: {jobname}")
        if (not args.dry_run):
            try:
                job = client.create_job(request)
                print(f"{jobname} was succesfully created")
            except Exception as e:
                print(f"Error while trying to create job {jobname}: {e}")
        else:
            print(f"Tried to launch: {jobname}")
        
    if not args.dry_run:
        print(f"Created {len(jobs)} jobs in Cloud Batch")

if __name__ == "__main__": 
    main()
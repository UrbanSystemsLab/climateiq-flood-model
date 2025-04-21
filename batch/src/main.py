import os
import argparse
import json
from google.cloud import batch_v1
from google.cloud import storage
from file_processing import process_jobs, clear_directory
from batch import create_job_request
import uuid
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
                        prog='FloodModel',
                        description='Launches Cloud Batch jobs')   
    parser.add_argument('-p', '--project_id', default='climateiq-test')
    parser.add_argument('-r', '--region_id', default='us-central1')
    parser.add_argument('--template_name', default='citycat_template.json')
    parser.add_argument('--dry_run', action=argparse.BooleanOptionalAction)
    parser.add_argument('--study_area', default='studyarea-1')
    parser.add_argument('--config', default="config-1")
    parser.add_argument('--input_bucket',  default='climateiq-flood-simulation-input-chunked')
    parser.add_argument('--configuration_bucket', default='climateiq-flood-simulation-config')
    parser.add_argument('--output_bucket',  default='climateiq-flood-simulation-output')
    parser.add_argument('--memory', choices=range(16,129),type=int,help="Value must be between 16 and 128", default=96)
    parser.add_argument('--repository_name', default='citycat-repository')

    args = parser.parse_args()
    print(f"Program arguments {args}")

    storage_client = storage.Client()
    input_bucket = storage_client.bucket(args.input_bucket)
    study_area_prefix = f"{args.study_area}/"
    blobs = input_bucket.list_blobs(prefix=study_area_prefix)
    chunk_directories = set()
    for blob in blobs:
        blob_name = blob.name
        relative_path = blob_name[len(study_area_prefix):]
        parts = relative_path.split('/')
        if len(parts) > 1:
            chunk_dir = parts[0]
            if chunk_dir.startswith('chunk_'):
                chunk_directories.add(chunk_dir)
    print(f"Found chunk directories: {chunk_directories}")
    # Read in template batch job.
    batch_directory = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(batch_directory, "template", args.template_name), 'r') as f:
        template = json.load(f)
        # Change the memory allocated.
        memory = str(int(args.memory * 1024)) 
        template["taskGroups"][0]["taskSpec"]["computeResource"]["memoryMib"] = memory
        template["allocationPolicy"]["instances"][0]["policy"]["machineType"] = "e2-custom-32-" + memory
        template["taskGroups"][0]["taskSpec"]["runnables"][0]["container"]["imageUri"] = f"{args.region_id}-docker.pkg.dev/{args.project_id}/{args.repository_name}/citycat-image:latest"
    # Read in the config.
    configs = []
    with open(os.path.join(batch_directory, "../config_uploader/out/", str(args.config) + ".txt"), 'r') as f:
        for line in f.readlines():
            _,c,_,r = line.split()
            configs.append({"CityCat_Config": c,  "Rainfall_Data": r})

    # Deletes anything previously in jobs directory
    jobs_directory = os.path.join(batch_directory, "jobs")
    Path(jobs_directory).mkdir(parents=True, exist_ok=True)
    clear_directory(jobs_directory)
    # Create jobs for each chunk directory
    for chunk_dir in chunk_directories:
        for config in configs:
            c = config["CityCat_Config"]
            r = config["Rainfall_Data"]
            job_uuid = uuid.uuid4().hex[:4]
            new_jobname = f"r{r}c{c}-{chunk_dir}-{args.config}-{job_uuid}"
            new_jobname = new_jobname.replace("_", "-").lower()
            with open(os.path.join(jobs_directory, f"{new_jobname}.json"), 'w+') as f:
                new_job = template.copy()
                new_job["name"] = new_jobname
                env_variables = new_job["taskGroups"][0]["taskSpec"]["runnables"][0]["environment"]["variables"]
                env_variables["CITYCAT_CONFIG_FILE"] = c
                env_variables["RAINFALL_DATA_FILE"] = r
                env_variables["CONFIG"] = str(args.config)
                env_variables["STUDY_AREA"] = f"{args.study_area}/{chunk_dir}"

            # Set buckets
                for volume in new_job["taskGroups"][0]["taskSpec"]["volumes"]:
                    mountpath = volume["mountPath"]
                    if mountpath == "/mnt/disks/share/climateiq-flood-simulation-input":
                        volume["gcs"]["remotePath"] = args.input_bucket
                    elif mountpath == "/mnt/disks/share/climateiq-flood-simulation-output":
                        volume["gcs"]["remotePath"] = args.output_bucket
                    elif mountpath == "/mnt/disks/share/climateiq-flood-simulation-config":
                        volume["gcs"]["remotePath"] = args.configuration_bucket
                json.dump(new_job, f, indent=1)
                     
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
    if not args.dry_run:
        print(f"Created {len(jobs)} jobs in Cloud Batch")

if __name__ == "__main__": 
    main()
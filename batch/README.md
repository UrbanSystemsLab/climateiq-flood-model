# Batch job 

## Install the requirements
- [ ] [gcloud CLI](https://cloud.google.com/sdk/docs/install)
- [ ] [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Make sure the repo is update
```
git pull upstream main
```

### Create a virtual environment 

#### For linux
```
cd batch
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

#### For windows 

```
cd batch
py -m venv env
env\Scripts\activate
py -m pip install -r requirements.txt
```

### Install gcloud CLI

Follow [instructions](https://cloud.google.com/sdk/docs/install-sdk)

Verify using

```
gcloud --help
```

Authenticate using:
```
gcloud auth application-default login
```

## To run

### For linux

```
cd batch
python3 src/main.py
python3 src/main.py --dry_run
python3 src/main.py --no-dry_run

# Set the study area and memory
python3 src/main.py --dry_run --study_area studyarea_2 --memory 128 --config 1

# A dry run to generate the configs
python3 src/main.py --dry_run --study_area Manhattan --config config_v1 --project_id climateiq_test
```

```
# To run all the jobs in the folder
python3 src/run_jobs.py --dry_run
python3 src/run_jobs.py --no-dry_run
```
### For windows 

```
cd batch
py src/main.py
py src/main.py --dry_run
py src/main.py --no-dry_run

# Set the study area and memory
py src/main.py --dry_run --study_area studyarea_2 --memory 128 --config 1 --project_id climateiq_test
```

## To cancel a job
```
gcloud batch jobs delete --location=us-central1 <job_name>
```

## To submit a single job
```
gcloud beta batch jobs submit r1c1-manhattan-config-v1-8266 --location=us-central1 --config=jobs/r1c1-manhattan-config-v1-8266.json
```

## Quotas

If you hit a quota max, try changing the regions

```
gcloud compute regions list
```

You should see a list like
```
us-central1              68/72   200/40960  3/69       0/21                UP
us-east1                 64/72   0/40960    2/69       0/21                UP
us-east4                 64/72   0/40960    2/69       0/21                UP
us-east5                 64/72   0/40960    2/69       0/21                UP
us-south1                64/72   0/40960    2/69       0/21                UP
us-west1                 97/100  10/40960   4/69       0/21                UP
us-west2                 64/72   0/40960    2/69       0/21                UP
us-west3                 64/72   0/40960    2/69       0/21                UP
us-west4                 64/72   0/40960    2/69       0/21                UP
```

The first column tells you the CPU usage and quota.

To run a job in a specific region use the script `run.sh` and to delete a job in a specific region use `delete.sh`

```
chmod +x scripts/run.sh 
chmod +x scripts/delete.sh 
```

Make sure to set the env variables correctly.

python config_uploader/main.py \
  --rainfall-directory /home/jainr/climateiq-flood-model/config_uploader/data/Rainfall_Scenarios_Atlas14_Atlanta \
  --configuration-name Atlanta_config \
  --batch-configuration-path out/Atlanta_batch_config_file \
  --configuration-bucket climateiq-flood-simulation-config
  python3 src/main.py --dry_run --study_area Atlanta --config Atlanta_config --project_id climateiq
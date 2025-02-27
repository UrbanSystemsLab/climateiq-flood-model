# Build and run the image locally

## To build the image

```
cd hecras-image
DOCKER_BUILDKIT=1 docker build --tag=hecras-image:latest .
```

**Note**: Make sure you are in the correct directory when you try to build the image.

## To run

**Note**: You need to download the hecras binaries and example Muncie from the bucket and place it under climateiq-flood-simulation-input before running the image.
cd climateiq-flood-simulation-input
gsutil -m cp -r gs://hecras-linux-bin


The following mounts the 3 local directories and uses the default environment variables and entry point.
```
docker run -it -v $(pwd)/climateiq-flood-simulation-input:/mnt/disks/share/climateiq-flood-simulation-input -v $(pwd)/climateiq-flood-simulation-output:/mnt/disks/share/climateiq-flood-simulation-output -v $(pwd)/climateiq-flood-simulation-config:/mnt/disks/share/climateiq-flood-simulation-config hecras-image:latest 
```

### Override env variables

Pass the command a `-e` flag.
```
docker run -it -e STUDY_AREA=manhattan -v $(pwd)/climateiq-flood-simulation-input:/mnt/disks/share/climateiq-flood-simulation-input -v $(pwd)/climateiq-flood-simulation-output:/mnt/disks/share/climateiq-flood-simulation-output -v $(pwd)/climateiq-flood-simulation-config:/mnt/disks/share/climateiq-flood-simulation-config hecras-image:latest  
```
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        ca-certificates \
        language-pack-en \
        language-pack-zh-han* \
        locales \
        locales-all \
        wget 

RUN apt-get install -y --no-install-recommends \
    vim \ 
    zip

#set env variable defaults
ENV INPUT_MOUNT_DIRECTORY=/mnt/disks/share/climateiq-flood-simulation-input
ENV CONFIG_MOUNT_DIRECTORY=/mnt/disks/share/climateiq-flood-simulation-config
ENV OUTPUT_MOUNT_DIRECTORY=/mnt/disks/share/climateiq-flood-simulation-output
ENV STUDY_AREA="Muncie"
ENV CONFIG="default_config"
ENV DRY_RUN=false

# Copy entrypoint script and run
WORKDIR /root
COPY execute.sh .
RUN chmod +x execute.sh

ENTRYPOINT ["bash", "/root/execute.sh"]

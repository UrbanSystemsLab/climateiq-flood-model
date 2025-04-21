# Partly from https://leimao.github.io/blog/Docker-Wine/
# Partly from https://github.com/OpenCLIM/citycat-dafni/blob/master/Dockerfile

FROM ubuntu:20.04

# Set environment for non-interactive installations
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        ca-certificates \
        locales \
        wget \
        vim \
        zip \
        xvfb \
        x11-utils \
        xdotool

# Configure locales
RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

# Install Wine
RUN dpkg --add-architecture i386 && \
    mkdir -pm755 /etc/apt/keyrings && \
    wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key && \
    wget -nc -P /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/$(lsb_release -sc)/winehq-$(lsb_release -sc).sources && \
    apt-get update -y --fix-missing && \
    apt-get install -y --install-recommends winehq-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set env variable defaults
ENV INPUT_MOUNT_DIRECTORY=/mnt/disks/share/climateiq-flood-simulation-input
ENV CONFIG_MOUNT_DIRECTORY=/mnt/disks/share/climateiq-flood-simulation-config
ENV OUTPUT_MOUNT_DIRECTORY=/mnt/disks/share/climateiq-flood-simulation-output
ENV STUDY_AREA="studyarea_1"
ENV CONFIG="config_1"
ENV CITYCAT_CONFIG_FILE=1
ENV RAINFALL_DATA_FILE=11
ENV DRY_RUN=false

# Copy entrypoint script and run
WORKDIR /root
COPY execute.sh .
RUN chmod +x execute.sh

ENTRYPOINT ["bash", "/root/execute.sh"]

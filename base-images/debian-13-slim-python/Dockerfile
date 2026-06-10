FROM debian:13-slim

USER root

# Add some tolerance to the apt system for Mac machines ...
# potential solutions:
# [failed] https://stackoverflow.com/questions/48645936/docker-for-mac-hash-sum-mismatch 
# [worked] https://stackoverflow.com/questions/67732260/how-to-fix-hash-sum-mismatch-in-docker-on-mac
#
RUN echo "Acquire::http::Pipeline-Depth 0;" > /etc/apt/apt.conf.d/99custom \
 && echo "Acquire::http::No-Cache true;"   >> /etc/apt/apt.conf.d/99custom \
 && echo "Acquire::BrokenProxy    true;"   >> /etc/apt/apt.conf.d/99custom

RUN apt update

ARG DEBIAN_FRONTEND=noninteractive

# Add all of the packages useful for the base image type - the devcontainer
# can be confired with additional packages if needed.
#
# See this note on how apt pinning works - we want to build containers
# with very specific versions, but also allow security updates so
# that a later container build doesn't break because of a patch.
#
# https://wiki.debian.org/AptConfiguration#Using_pinning
#
COPY apt.preferences /etc/apt/preferences

RUN apt install --no-install-recommends -y \
        ca-certificates \
        tzdata \
        locales \
        git \
        ssh \
        make \
        python3 \
        python3-clang \
        python3-pip \
        python3-sphinx \
        python3-sphinx-rtd-theme \
        python3-sphinxcontrib.plantuml \
        graphviz \
        default-jre \
        vim \
        bash-completion \
        wget
 
RUN wget -P /opt -x -nH --cut-dirs=1 \
    https://github.com/plantuml/plantuml/releases/download/v1.2025.9/plantuml-1.2025.9.jar \
 && ln -s /opt/plantuml/releases/download/v1.2025.9/plantuml-1.2025.9.jar /opt/plantuml/plantuml.jar

# Prepare to install all the additional Python packages
#
COPY requirements.txt /tmp/requirements.txt

# Debian uses externally managed Python3 - so installing system-wide
# may break system packages. This is a container, and we can force
# specific package versions if needed in the requirements.txt file.
#
RUN pip3 install --break-system-packages -r /tmp/requirements.txt

# Clean up the apt cache and lists to save space in the image
#
RUN apt -y autopurge \
 && apt -y autoclean \
 && apt -y autoremove \
 && rm -rf /var/lib/apt/lists/*

# NOTE: The default user for this image is still root!
#
# It is up to you to change this to a more sane value when you
# build the devcontainer.

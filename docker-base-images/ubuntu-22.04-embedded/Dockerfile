FROM ubuntu:22.04

USER root

# The Ubuntu Docker images after 22.04 have a default "ubuntu" user
# so we need to create one here to make sure that more up to date .devcontainers
# don't break.
#
ARG USER_NAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
#
RUN groupadd --gid $USER_GID $USER_NAME \
 && useradd --uid $USER_UID --gid $USER_GID -d /home/$USER_NAME -m -s /usr/bin/bash $USER_NAME

# Add some tolerance to the apt system ...
# potential solutions:
# [failed] https://stackoverflow.com/questions/48645936/docker-for-mac-hash-sum-mismatch 
# [worked] https://stackoverflow.com/questions/67732260/how-to-fix-hash-sum-mismatch-in-docker-on-mac
# 
RUN echo "Acquire::http::Pipeline-Depth 0;" > /etc/apt/apt.conf.d/99custom \
 && echo "Acquire::http::No-Cache true;"   >> /etc/apt/apt.conf.d/99custom \
 && echo "Acquire::BrokenProxy    true;"   >> /etc/apt/apt.conf.d/99custom

RUN apt update

ARG DEBIAN_FRONTEND=noninteractive

# Add all of the stuff needed to build an embedded target in a
# Docker container. Note that the debugger hardware runs on
# the host, not in the container.
#
# See this note on how apt pinning works - we want to build containers
# with very specific versions, but also allow security updates so
# that a later container build doesn't break because of a patch.
#
# https://help.ubuntu.com/community/PinningHowto
#
COPY apt.preferences /etc/apt/preferences

RUN apt install --no-install-recommends -y \
        ca-certificates \
        tzdata \
        locales \
        git \
        ssh \
        python3 \
        build-essential \
        gcc-arm-none-eabi \
        picolibc-arm-none-eabi \
        gdb-multiarch \
        binutils-multiarch-dev \
        python3-clang \
        python3-pip \
        python3-sphinx \
        lcov \
        cpputest \
        graphviz \
        default-jre \
        vim \
        bash-completion \
        wget

RUN ln -s /usr/bin/gdb-multiarch /usr/bin/arm-none-eabi-gdb \
 && ln -s /usr/bin/nm /usr/bin/nm-multiarch \
 && ln -s /usr/bin/objdump /usr/bin/objdump-multiarch

RUN wget -P /opt -x -nH --cut-dirs=1 \
      https://github.com/plantuml/plantuml/releases/download/v1.2024.6/plantuml-1.2024.6.jar \
 && ln -s /opt/plantuml/releases/download/v1.2024.6/plantuml-1.2024.6.jar /opt/plantuml/plantuml.jar

# Now install all the additional Python packages
#
COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

# Clean up the apt cache and lists to save space in the image
#
RUN apt -y autopurge && \
    apt -y autoclean && \
    apt -y autoremove && \
    rm -rf /var/lib/apt/lists/*

# NOTE: The default user for this image is still root!
#
# It is up to you to change this to a more sane value when you
# build the devcontainer.

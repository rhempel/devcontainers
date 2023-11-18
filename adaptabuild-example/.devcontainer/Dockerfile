FROM ubuntu:22.04

# Note: The GID is super critical to get right - on my Linux machine it does
#       not seem to matter, but on Windows I believe it requires the GID to
#       match your UID in the WSL system?

ARG USERNAME=adaptabuild
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -d /home/$USERNAME -m -s /usr/bin/bash $USERNAME

# [Optional] Add sudo support. Omit if you don't need to install software after connecting.
RUN apt update && \
    apt install  --no-install-recommends -y sudo && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Add a layer with the correct locale and timezone

ENV LANG en_US.UTF-8
ENV TZ Etc/EST

ARG DEBIAN_FRONTEND=noninteractive

# For more information on managing locales in mimimal Ubuntu docker
# images, see: https://hub.docker.com/_/ubuntu

RUN apt install --no-install-recommends -y \
                   tzdata \
                   locales && \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

# Add all of the stuff needed to build an embedded target in a
# Docker container. Note that the debugger hardware runs on
# the host, not in the container.
#
# NOTE: Sometimes this step fails if Ubuntu has released a security update
#       for a package in this list. You may need to run:
#
#       sudo apt-cache policy packagename
#
#       to get a list of up to date candidates.

RUN apt install --no-install-recommends -y \
                   git=1:2.34.1-1ubuntu1.9 \
                   ssh=1:8.9p1-3ubuntu0.4 \
                   python3=3.10.6-1~22.04 \
                   build-essential=12.9ubuntu3 \
                   gcc-arm-none-eabi=15:10.3-2021.07-4 \
                   gdb-multiarch=12.1-0ubuntu1~22.04 \
                   binutils-multiarch=2.38-4ubuntu2.3 \
                   python3-clang=1:14.0-55~exp2 \
                   python3-pip=22.0.2+dfsg-1ubuntu0.4 \
                   python3-sphinx=4.3.2-1 \
                   lcov=1.15-1 \
                   cpputest=4.0-2 \
                   graphviz=2.42.2-6 \
                   default-jre=2:1.11-72build2 \
                   vim=2:8.2.3995-1ubuntu2.13 \
                   wget=1.21.2-2ubuntu1 && \
    ln -s /usr/bin/gdb-multiarch /usr/bin/arm-none-eabi-gdb && \
    wget -P /opt -x -nH --cut-dirs=1  https://github.com/plantuml/plantuml/releases/download/v1.2023.11/plantuml-1.2023.11.jar

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

# Don't do this until we are ready to rebuild the machine a final time
# RUN apt -y autopurge && \
#     apt -y autoclean && \
#     apt -y autoremove && \
#     rm -rf /var/lib/apt/lists/*

# [Optional] Set the default user - omit if you want to keep
# the default as root. (You don't)

USER $USERNAME

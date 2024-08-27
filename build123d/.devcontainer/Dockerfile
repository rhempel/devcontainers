FROM python:3.11.5-bookworm

ARG USERNAME=build123d
ARG USER_UID=2000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# [Optional] Add sudo support. Omit if you don't need to install software after connecting.
RUN apt update && \
    apt install -y sudo && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Add a layer with the correct locale and timezone

ENV LANG en_US.UTF-8
ENV TZ Etc/EST

ARG DEBIAN_FRONTEND=noninteractive

RUN apt install -y libgl1-mesa-glx 

RUN python3 -m pip install git+https://github.com/gumyr/build123d

# [Optional] Set the default user. Omit if you want to keep the default as root.

USER $USERNAME

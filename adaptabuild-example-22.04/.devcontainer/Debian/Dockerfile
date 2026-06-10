FROM debian-13-embedded

# Note: The GID is super critical to get right - on my Linux machine it does
#       not seem to matter, but on Windows I believe it requires the GID to
#       match your UID in the WSL system?
#
# NOTE : The ARG values below can be overridden in the devcontainer.json
#        file - don't touch the defaults in this file
#
ARG USER_NAME=debian
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG USER_LANG=en_US.UTF-8
ARG USER_TZ=Etc/EST

# Create our user.
#
# Creating the mail folder is only to avoid a harmless error message about a missing
# mail spooler file when we delete the default ubuntu user. 
#
RUN groupadd -o --gid $USER_GID $USER_NAME \
 && useradd --uid $USER_UID --gid $USER_GID -d /home/$USER_NAME -m -s /usr/bin/bash $USER_NAME

# RUN apt update
# 
# # [Optional] Add sudo support - omit if you don't need sudo privileges during
# #            development.
# #
# RUN apt install --no-install-recommends -y sudo \
#  && echo $USER_NAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USER_NAME \
#  && chmod 0440 /etc/sudoers.d/$USER_NAME
# 
# # Add a layer with the correct locale and timezone
# #
# ENV LANG=$USER_LANG
# ENV TZ=$USER_TZ
# 
# ARG DEBIAN_FRONTEND=noninteractive
# 
# # For more information on managing locales in mimimal Ubuntu docker
# # images, see: https://hub.docker.com/_/ubuntu
# #
# # NOTE: This is where we might need to separate the locale, character map, and encoding
# #
# RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

# Set the default user - omit if you want to keep the default
# as root. (You don't)
#
USER $USER_NAME

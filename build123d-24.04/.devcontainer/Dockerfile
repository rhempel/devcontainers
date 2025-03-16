FROM ubuntu-24.04-python

# Note: The GID is super critical to get right - on my Linux machine it does
#       not seem to matter, but on Windows I believe it requires the GID to
#       match your UID in the WSL system?
#
# Note: The ubuntu:24.04 Docker image now includes a default user "ubuntu"
#       with a UID/GID of 1000.
#
# For consistency, with 24.04, our ubuntu-embedded:22.04 image also has a
# default "ubuntu" user. 
#
# See this StackOverflow page for the implications:
# https://askubuntu.com/questions/1513927/ubuntu-24-04-docker-images-now-includes-user-ubuntu-with-uid-gid-1000
#
# NOTE : The ARG values below can be overridden in the devcontainer.json
#        file - don't touch the defaults in this file
#
ARG USER_NAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG USER_LANG=en_US.UTF-8
ARG USER_TZ=Etc/EST

# Delete the default Ubuntu user then create our user.
#
# Creating the mail folder is only to avoid a harmless error message about a missing
# mail spooler file when we delete the default ubuntu user. 
#
RUN touch -f /var/mail/ubuntu \
 && chown ubuntu /var/mail/ubuntu \
 && userdel -r ubuntu \
 && useradd -d /home/$USER_NAME -m -s /usr/bin/bash $USER_NAME

# && groupadd -o --gid $USER_GID $USER_NAME \
# && useradd --uid $USER_UID --gid $USER_GID -d /home/$USER_NAME -m -s /usr/bin/bash $USER_NAME

RUN apt update

# [Optional] Add sudo support - omit if you don't need sudo privileges during
#            development.
#
RUN apt install --no-install-recommends -y sudo \
 && echo $USER_NAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USER_NAME \
 && chmod 0440 /etc/sudoers.d/$USER_NAME

# Here's what build123d needs ...

RUN apt install --no-install-recommends -y python3-asttokens \
                                           python3-contourpy \
                                           python3-cycler \
                                           python3-decorator \
                                           python3-executing \
                                           python3-ezdxf \
                                           python3-ipykernel \
                                           python3-ipython \
                                           python3-jedi \
                                           python3-jupyter-console \
                                           python3-matplotlib \
                                           python3-matplotlib-inline \
                                           python3-parso \
                                           python3-pexpect \
                                           python3-ptyprocess \
                                           python3-pyparsing \
                                           python3-scipy \
                                           python3-svgelements \
                                           python3-svgwrite \
                                           python3-traitlets \
                                           python3-vtk9 \
                                           python3-wcwidth

# Now remove the packages that will conflict with build123d

RUN apt remove -y python3-numpy \
                  python3-kiwisolver

# And install build123d

RUN pip install --break-system-packages pandas-stubs build123d ocp_vscode

# Add a layer with the correct locale and timezone
#
ENV LANG=$USER_LANG
ENV TZ=$USER_TZ

ARG DEBIAN_FRONTEND=noninteractive

# For more information on managing locales in mimimal Ubuntu docker
# images, see: https://hub.docker.com/_/ubuntu
#
# NOTE: This is where we might need to separate the locale, character map, and encoding
#
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

# Set the default user - omit if you want to keep the default
# as root. (You don't)
#
USER $USER_NAME

----------------------

Set your defaulkt timezone in containers.conf

-----------------------

investigate overriding userns=host

-----------------------

For ssh access, need to create /etc/ssh/ssh_config.d/30-userlist.conf
and add

AllowUsers username

then

sudo /etc/init.d/ssh restart

-----------------------

To add your authorized keys ...

(umask 177 && cat ~/.ssh/id_hempelra.pub  > ~/.ssh/authorized_keys)

cd C:\Users\HempelRa\Projects\devcontainers\rhempel-docker-devcontainers


podman buildx build -t debian-13-slim-build123d base-images/debian-13-slim-build123d

podman buildx build \
    -t build123d-debian-13 \
    --build-arg USER_NAME=$USER \
    --build-arg USER_UID=1000 \
    --build-arg USER_GID=1000 \
    --build-arg USER_LANG=en_US.UTF-8 \
    --build-arg USER_TZ=local \
    build123d-debian-13/.devcontainer

podman create -it \
           --user $USER:$USER \
           --publish 22003:22 \
           --volume build123d-debian-13-volume:/home/$USER/projects \
           --volume ./build123d-debian-13/.devcontainer:/home/$USER/.devcontainer:O \
           --volume $HOME/.ssh:/home/$USER/.ssh:O \
           build123d-debian-13 bash --rcfile /home/$USER/.devcontainer/commands/postStartCommand.sh

#            --publish 127.0.0.1:3939:3939 \

podman machine start

podman start -ai 3ff663a



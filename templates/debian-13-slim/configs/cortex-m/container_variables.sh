# -----------------------------------------------------------------------------
container_user=${USER}

container_port_maps=("0.0.0.0:22002:22")

container_volume_maps=("${container_tagname}-volume:/home/${container_user}/projects" \
                       "/home/${container_user}/.ssh:/home/${container_user}/.ssh:O" \
                       "/home/${container_user}/.gitconfig:/home/${container_user}/.gitconfig")

container_host_maps=("host.gdb.gateway:host-gateway" \
                     "C9YSTQ3.gdb.gateway:192.168.2.23")

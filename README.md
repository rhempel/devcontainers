## Introduction

This repository holds Podman container support files
that let you create and manage general purpose environments
that can be extended as needed for specific use cases.

Why is this important?

With the increasing complexity of managing your development
environment, it's becoming more likely that an upgrade a package
or application and its support libraries might cause other
software on your system to break.

One option is to have multiple computers that do only one thing, but
that's wasteful in terms of energy, space, and money because most
of the time they will be sitting idle.

Containers make it relatively easy to set up and maintain single
purpose computers that you "spin up" on your host machine as
needed. You might think that you need a heavy-duty host computer
to pull this off, but I've done this on a 10 year old laptop with
4 GB RAM and a 128 GB SSD. My long term test system is an 8th Gen
i5 mini-PC with 16GB of RAM and a 512 GB SSD.

Long story short, containers make it possible to keep your daily
driver computer insulated from your software experiments. They
also support the idea of "infrastructure as code" - which means you
can avoid lengthy descriptions of how to set up a dedicated machine
and instead use scripts to do it automagically.

## Podman and VSCodium

We focus on Podman as the container engine and VSCodium as the container
management tool, but the same concepts apply to Docker and VSCode.
Podman documentation refers to `Containerfile` interchangeably with
`Dockerfile`. We will use Podman terminology moving forward.

The process for creating and managing containers is the same on
Linux, MacOS, Windows, and eventually *BSD when I get around to
testing that.

:exclamation: The files in this repository should be considered as
a starting point for your own container management needs. They help
me to build containers for embedded systems and Python development.

:exclamation: Currently I only have the Linux build scripts in place, the
Windows and MacOS scripts are under development.

:exclamation: Running containers on Windows is a little different - so
    be sure to read these exclamations carefully!

The following terms are important:

| Term         | Description |
| -            | -           |
| Image        | The template for a container - you can re-use the same image for multiple containers.
| Container    | An instance of an image that is configured for a specific task.
| Volume       | A file system that can be attached to a running container
| Devcontainer | A Microsoft specific variant of a container that VSCode can manipulate directly. We can get most of the devcontainer features in other ways with Podman.

## Install a Container Environment

If you have not already done so, install Podman. There is no need to install
the ``-desktop`` variant of the container environment. We will be doing our
work from the command line and then using VSCodium to interact with Podman.

- [Podman Windows and MacOS Install]
- [Podman Linux Install]
- [Podman FreeBSD Install]

On Windows, read and follow the instructions for using the WSL system
with your containerization environnment, including any computer restarts.

### Windows/MacOS Post--Install Instructions for Podman

For the highest level of security, we want to run our Podman containers
as rootless and with user mode networking. User mode networking is the
default for Linux so we might as well set it up that way on Windows and
MacOS to minimize differences. Open a command prompt and run:

```
podman machine stop
podman machine set --rootful=false
podman machine set --user-mode-networking=true
podman machine start
```

## Add Plugins To VSCodium

I generally avoid GUI based management tools for things like Podman for
two reasons. First, the UI often changes and that makes it hard to keep
instructions up to date. Second, the GUI is yet another layer of complexity
that can make your use of the tool unreliable. Third, using the command
line to interact with your tools means that you can automate instead of
pointing and clicking.

That being said, the following plugins for VSCodium are recommended:

| Plugin | Description |
| -      | -           |
| [Remote Explorer][Remote Explorer Plugin]  (jeanp413) | Access to containers and remote computers from your host |
| [Container Tools][Container Tools Plugin] (ms-azuretools) | View and control containers, volumes, and images |
| [Compare Folders][Compare Folders Plugin] (moshfeu) | Compare files and folders across the network |

## Podman Image Overview

At one point, I advocated for building base images, and then building
the final image that would eventually be used to create the container.
It turns out that this step wasn't adding any real value and was making
things more complicated.

Instead we are now recommending a single step to build the image and
then creating the container. Note that we don't have to create a new
container very often in our use case. It's more like a separate
computer that lives on our host, and that is guaranteed to have the same
software on it, not matter who builds it. We can start and stop it
at any time, just like a real computer.

Let's start with a simple container - one that we can use to
verify that we can reliably build container images. This is also
an opportunity to point out some best practices for container management
with Podman.

### Container Build System Folder Structure

One thing we can do to simplify container management is to adopt a naming
convention. In the example folder structure below we use the following
common container descriptor names and definitions:

| Name | Example | Description |
| -    | -       | -           |
| Name | `debian` | The name of the container base image (default is `debian`)
| Tag | `13-slim` | The tag of the container base image (default is `latest`)
| Variant | `default` | The configuration variant of the new container (default is `default`)

First, we will review the directories and files that define how are containers
are built.

```
 +-scripts
 | +-windows
 | +-linux
 |   +-create_container.sh
 |   +-build_image.sh
 +-templates
 | +-debian-13-slim
 |   +-Containerfile
 |   +-configs
 |   | +-default
 |   | | +-container_variables.sh
 |   | | +-scripts
 |   | |   +-postAttachCommand
 |   | |   +-postCreateCommand
 |   | |   +-postStartCommand
 |   | +-sphinx
 |   |   +-container_variables.sh
 |   |   +-scripts
 |   |     +-postAttachCommand
 |   |     +-postCreateCommand
 |   |     +-postStartCommand
 |   +-etc
 |     +-apt
 |       +-preferences.d
 |       | +-99container.pref
 |       +-apt.conf.d
 |         +-99toleratehashmismatch
 +-LICENSE.md
 +-README.md
```

In our example filesystem, we are using `debian-13-slim` as the base image, and we support two variants.
The first is `default` - a minimal container demonstrating best practices for configuration. The
second is `sphinx` - a container that supports Python development together with Sphinx for building
documentation.

This table describes the purpose of each folder ...

| Folder | Description |
| -      | -           |
| `scripts` | Container build scripts for supported host platforms
| `scripts/linux` | Container build scripts for Linux host platforms
| `templates` | Template files for container images and instances
| `templates/debian-13-slim` | Template files for `debian-13-slim` containers
| `templates/debian-13-slim/Containerfile` | Build instructions for `debian-13-slim` containers
| `templates/debian-13-slim/configs` | Build configurations for `debian-13-slim` variants
| `templates/debian-13-slim/configs/default` | Build configurations for `debian-13-slim-default`
| `templates/debian-13-slim/configs/sphinx` | Build configurations for `debian-13-slim-sphinx`
| `templates/debian-13-slim/etc` | Files to copy to `debian-13-slim` containers
| `templates/debian-13-slim/etc/apt` | Configuration for `apt` in `debian-13-slim` containers

### Scripting How The Container Behaves

The `scripts` folder in any container variant folder holds at least these
files that are copied to the container under `/etc/devcontainer` as part of the
container image creation process.

| File | Description |
| -      | -          |
| `postCreateCommand` | Runs as `root` once after the container image is created. No volumes are mounted yet!
| `postStartCommand`  | Runs as the default user every time the container is started. Volumes are mounted.
| `postAttachCommand` | Runs as the default user every time a shell is attached to the container

#### Using `postCreateCommand`

This file runs as `root` just before we switch to the default user at container
image creation time. Besides installing any packages needed for the container to
do useful work, this script also sets up a soft link for the `postAttachCommand` so
that it's executed as part of attaching a login shell to the container.

```
ln -s /etc/devcontainer/postAttachCommand /etc/profile.d/99postAttachCommand.sh
```

#### Using `postStartCommand`

This file runs as the default user when the container instance is started. Any
volume mounts and network port mapping is in place when the script runs. The default
user should be set up to have `sudo` privileges as part of the container setup.

The `postStartCommand` file performs a number of tasks, such as making sure that the
volume that is mounted under `~/projects` is owned by the container user:

```
# Put the current user into an environment variable. Containers
# run with the login user "root" running as whatever the USER varaible
# is set to in the Dockerfile
#
export WHOAMI=$(whoami)

cd ~

# The volume that is mounted to ~/projects is created automatically
# if it does not exist when the container is created, and the mount
# point is owned by root.
#
# Now set the correct ownership of ~/projects
#
sudo chown ${WHOAMI}:${WHOAMI} projects
```

It also sets up the `~/.ssh` folder to have the correct permissions. Recall
that as an overlay, it is owned by `root` so we need to set the ownership to
the correct user and update the permissions to be compatible with the `ssh`
program requirements.

We can also add our public key to our overlay of the `authorized_keys` file
and add ourselves to the allowed users for `ssh` without changing anything
on the host. That will let us `ssh` in to the running container.

```
chmod 700 .ssh
chmod 600 .ssh/*
chmod 644 .ssh/*.pub

# Create the authorized_keys file, then append the keys that
# you want to authorize for this container.
#
(umask 177 && touch -c .ssh/authorized_keys)
cat .ssh/id_hempelra.pub >> .ssh/authorized_keys

# Now update the ssh_config.d folder with a file that will allow
# our user to access the container over ssh
#
sudo sh -c "echo 'AllowUsers ${WHOAMI}' > /etc/ssh/sshd_config.d/30-${WHOAMI}.conf"
sudo /etc/init.d/ssh restart
```

#### Using `postAttachCommand`

This script runs every time we attach a login shell to the container. It's
where I put anything that needs to run to set up my environment, such as
changing to a default directory, setting up a prompt string, or anything
else that I don't want to handle manually.

### Container Build Variants

Creating a new configuration variant `foo` for an existing container template
is just two steps:

1. Copy the `templates\Name-Tag\configs\default` contents
   to a new `templates\Name-Tag\configs\foo` folder
2. Modify the `container_variables` and `scripts\*`
   contents to suit your needs.

Creating a new container template is a little more involved. This might
happen if you need to change or upgrade the Linux distribution your containers
are based on.

You will need to copy `templates/Name-Tag` to a new folder and update
the `Containerfile` and variant files to support your new target
distribution.

### Building and Starting A Container

Within the `scripts` folder for supported host platforms, we have the following:

| File | Description |
| -      | -           |
| `build_image` | Builds a container image on a Linux host
| `create_container` | Creates a container instance on a Linux host

Building our `debian-13-slim-default` container is a two-step process:

```
build_image -t debian-13-slim -c default
create_container -t debian-13-slim -c default
```

The result is a container that can be started using:

```
podman start -ai debian-13-slim-default
```

The `-ai` option attaches the container’s `stdout`, `stderr`, and `stdin`
to an interactive session. Basically, you get a terminal session to your
running container.

From this point forward, it's like having a new computer dedicated
to a specific task. As long as you store your work under `~/projects`
you can destroy the container and rebuild it without losing any work because
it's stored in a volume separate from the container contents.

## Next Steps - Best Practices for Container Environments

Now that we have verified a minimal container and image build, we
can describe some of the practices that I have found to be helpful
for my use cases.

You may have different needs for security or networking, so study
the documentation for your container management system and review
other sources to make the choices that are best for you.

I normally use a container as a dedicated computer with command-line
shell access - connecting VSCodium to the container working with that
as my IDE. Let's see how I make that as painless as possible.

### Add A non-root User During Image Build

The first thing we will do is add a non-root user, and install the `sudo`
package. To make the `Containerfile` script a bit more general, we have added
a number of build-time arguments that can be overridden on the build command line.

```
ARG USER_NAME=debian
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG USER_LANG=en_US.UTF-8
ARG USER_TZ=Etc/EST
ARG USER_SHELL=/usr/bin/bash
```

The defaults make it so the only thing we need to override in the
``container_variables.sh` file is the value of `container_user` to
be used to override the default `USER_NAME`.

You (or whichever `USER_NAME` you specified) are now the default user in
the running container, and that you have passwordless `sudo` access. Use
it appropriately!

The container starts in the root (`/`) directory, which may not be convenient
but we can change that in the `postAttachCommand` file. The remaining customizations
are made at container creation time.

### Configure `ssh` For The Container User

My container setup adds a non-root user with my host username that has access
to passwordless `sudo`. When I am using the container, I want to
be able to access `git` and other tools that need `ssh` as if I was on my
host machine.

It's not a good idea to copy your private `~/.ssh` folder to a container
because that becomes a permanent part of the container contents. Instead,
I use an *overlay* mount to make my host user's `~/.ssh` folder available
to my container user. The overlay feature allows me to make changes to things
like the `known_hosts` or `authorized_keys` files in the container without
changing them on the host. When the container exits, the contents of the
overlay are lost. That means that any changes to the `~/.ssh` contents have to
be made each time the container is started ... and we'll talk about that
shortly.

The `~/.ssh` overlay volume is configured by this line in the
`container_variables.sh` file:

```
container_volume_maps=( ... \
                        "/home/${container_user}/.ssh:/home/${container_user}/.ssh:O" ) \
                        ... )
```

We're assuming that the `${container_user}` is the same on the host and
container. If not, just change the volume map to reflect your use case.

### Use Volume Mounts for Working Data

You might want to update a container image by adding a missing package
or changing how it is configured. It is easy to forget to back up
your work outside of the container and only realize it after cleaning up
or replacing the old container.

To avoid this, it is highly recommended to use an external volume mount
to hold workfiles. Note that this doesn't require you to repartition your
hard drive to add a mount point - the volume exists as a single file
that containers know how to mount and use.

This also keeps the size of your containers smaller - and you can mount
the same volume on multiple containers simultaneously as long as you are
careful about who gets read-only and write access.

The shared volume is configured by this line in the
`container_variables.sh` file. You can adjust the name(s) of the volume(s)
and the mount point(s) to suit your own needs.

```
container_volume_maps=( ... \
                        "${container_tagname}-volume:/home/${container_user}/projects" \
                        ... )
```

### `apt` Pinning - Ensure Secure and Repeatable Images

One of the problems we are trying to solve with containers is a repeatable
build environment. This can avoid "it works on my machine" problems and
keeps the development team happy. It also keeps the legacy support team
happy because they can recreate the build environment.

This is true for as long as your container image repository is around, and
for as long as the the Linux distro provides a package manager, and for as long
as package maintainers keep the packages available.

For this reason, it is HIGHLY recommended that your team keeps an
archive of mission critical Podman images and containers somewhere
safe. For more details on saving images read the
[Podman CLI reference for `image save`][Podman image save]

The `postCreateCommand` is where we specify which packages are to be added
the base image - but how do we ensure that the package versions
stay stable, and still receive security updates? The secret lies
in [`apt` pinning][apt-pinning]

We want to make sure that specific versions of the essential packages
are retreived, but the Debian (or other Debian based distros) do provide
security updates from time to time. In the past this meant updating the
`Containerfile` with more specific version strings, but now we encapsulate
this in the `apt.preferences` file that is copied to `/etc/apt` in the image creation
step.

A good example is the `ssh` package, it's at the heart of your container
network access security management. Here is the section from
`apt.preferences` for that package:

```
Package: ssh
Pin: version 1:10.0*
Pin-Priority: 1000
```

This says that version `1:10.0` followed by any additional characters
will be installed. The whole point of the `apt` package manager is
to keep your system up to date. Currently the preferred version of the
`ssh` package for Debian 13 is:

```
trixie (stable) (net): secure shell client and server (metapackage)
1:10.0p1-7+deb13u4: all
```

When a security update is made, any old package versions are *deleted* from
the Ubuntu package manager - this makes sense because you don't want to
install a package version with a known security issue.

As long as the Debian package maintainers keep the version of
`ssh` at `1:10.0` we are good. Debian Trixie is the current stable
release, so we can be confident that the version number of `ssh`
is unlikely to change, except for security patches.

[Docker]: https://docs.docker.com
[Podman]: https://podman.io/
[Docker buildx]: https://docs.docker.com/reference/cli/docker/buildx/build
[Podman build]: https://docs.podman.io/en/latest/markdown/podman-build.1.html
[Docker Windows Install]: https://docs.docker.com/desktop/setup/install/windows-install/
[Podman Windows and MacOS Install]: ​https://podman.io/docs/installation#installing-on-mac--windows
[Podman Linux Install]: https://podman.io/docs/installation#installing-on-linux
[Podman FreeBSD Install]: https://podman.io/docs/installation#installing-on-freebsd
[Remote Explorer Plugin]: https://open-vsx.org/vscode/item?itemName=jeanp413.open-remote-ssh
[Compare Folders Plugin]: https://open-vsx.org/vscode/item?itemName=moshfeu.compare-folders
[Container Tools Plugin]: https://open-vsx.org/vscode/item?itemName=ms-azuretools.vscode-containers
[Docker tag]: https://docs.docker.com/reference/cli/docker/image/tag
[Podman tag]: https://docs.podman.io/en/latest/markdown/podman-tag.1.html
[Docker image save]: https://docs.docker.com/reference/cli/docker/image/save
[Podman image save]: https://docs.podman.io/en/latest/markdown/podman-save.1.html
[apt-pinning]:  https://help.ubuntu.com/community/PinningHowto
[how-containers-work]: https://jvns.ca/blog/2020/04/27/new-zine-how-containers-work/
[container-names]: https://github.com/moby/moby/blob/master/pkg/namesgenerator/names-generator.go
[VSCode Remote Explorer]: https://marketplace.visualstudio.com/items?itemName=ms-vscode.remote-explorer
[VSCode DevContainer]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
[VSCode Docker]: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker
[podman host networking]: https://stackoverflow.com/questions/79098571/podman-container-cannot-connect-to-windows-host
[StackOverflow Anton]: https://stackoverflow.com/users/5788429/anton
[OpenOCD]: https://openocd.org/
[What is Podman]: https://www.redhat.com/en/topics/containers/what-is-podman#why-podman
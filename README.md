BREAK THIS DOCUMENT INTO TWO PARTS:

1. GETTING STARTED WITH PODMAN/VSCODIUM
2. 

## Introduction

This repository holds Podman container build scripts
that let you create and manage general purpose environments
that can be extended as needed for specific use cases.

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
Windows and MacOS scripts are under development. I'm looking at using `jq`
as an external parser for JSON files that describe the container options.

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

## Podman Image Builds

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
common names and definitions:

| Name | Example | Description |
| -    | -       | -           |
| Container Name | `debian` | The name of the container base image
| Container Tag | `13-slim` | The tag of the container base image (default is `latest`)
| Container Variant | `sphinx` | The configuration variant of the new container (default is `default`)




Container build script variables for a container variant


First, we will review the directories and files that define how are containers
are built.

```
 +-configs
 | +-debian-13-slim-default
 | +-debian-13-slim-sphinx
 +-scripts
 | +-windows
 | +-linux
 |   +-create_container.sh
 |   +-build_image.sh
 +-templates
 | +-debian-13-slim
 |   +-Containerfile
 |   +-etc
 |     +-devcontainer
 |     | +-default
 |     | | +-postAttachCommand
 |     | | +-postCreateCommand
 |     | | +-postStartCommand
 |     | +-sphinx
 |     |   +-postAttachCommand
 |     |   +-postCreateCommand
 |     |   +-postStartCommand
 |     +-apt
 |       +-preferences.d
 |       | +-99container.pref
 |       +-apt.conf.d
 |         +-99toleratehashmismatch
 +-LICENSE.md
 +-README.md
```

In our example filesystem, we are using `debian-13-slim` as the base image, and we support two variants.
The first is `default` - a minimal container demonstrating best practices for configuraiton. The
second is `sphinx` - a container that supports Python development together with Sphinx for building
documentation.

This table describes the purpose of each folder ...

| Folder | Description |
| -      | -           |
| `configs` | Container build script variables for a container variant
| `configs/debian-13-slim-default` | Container build script variables for the `default` variant of `debian-13-slim`
| `configs/debian-13-slim-sphinx` | Container build script variables for the `sphinx` variant of `debian-13-slim`
| `scripts` | Container build scripts for supported host platforms
| `scripts/linux` | Container build scripts for Linux host platforms
| `templates` | Template files for container images and instances
| `templates/debian-13-slim` | Template files for `debian-13-slim` containers
| `templates/debian-13-slim/Containerfile` | Build instructions for `debian-13-slim` containers
| `templates/debian-13-slim/etc` | Configuration files for `debian-13-slim` containers
| `templates/debian-13-slim/etc/apt` | Configuration for `apt` in `debian-13-slim` containers
| `templates/debian-13-slim/etc/devcontainer` | Configuration for `debian-13-slim` container variants
| `templates/debian-13-slim/etc/devcontainer/default` | Configuration for `debian-13-slim` default container
| `templates/debian-13-slim/etc/devcontainer/sphinx` | Configuration for `debian-13-slim` Sphinx container

### Building A Container

Within the `scripts` folder for supported host platforms, we have the following scripts:

| File | Description |
| -      | -           |
| `build_image.sh` | Builds a container image on a Linux host
| `create_container.sh` | Creates a container instance on a Linux host



 | Access to containers and remote computers from your host |
| [Container Tools][Container Tools Plugin] (ms-azuretools) | View and control containers, volumes, and images |
| [Compare Folders][Compare Folders Plugin] (moshfeu) | Compare files and folders across the network |

<!-- ============================================================================
# We are now ready to begin building a base image that can be used to
# build a devcontainer. Why use base images? Mainly to speed up the
# creation of multiple devcontainers using a common base image and to
# avoid duplication.
# 
# For example, I do embedded systems development in C, and also
# tasks like writing for my website or 3D modelling that use
# Python but don't need the C compiler. It makes sense to have
# two base images, one for embedded development and one for Python.
# I can then quickly create a task-specific devcontainer with just a few
# additions.
# 
# Containers are awesome tools to simplify your development process. To
# learn more about how they work, I can recommend [this 'zine by Julia
# Evans][how-containers-work].
# 
# If you have ever wondered how containers get their default names, then
# [this file][container-names] will be interesting.
# 
# ### Starting a Base Image Build
============================================================================= -->

Docker and Podman have almost identical command lines. This is by design as
Podman came after Docker. Rather than develop yet another _almost_ compatible
command line, the Podman team wisely chose to simply duplicate the semantics
of Docker. They even went so far as to be able to read the Dockerfile format.

| Environment | Version | Notes |
| -           | - | - |
| Docker      | 4.32.0+ | The traditional `build` command is now legacy, so we use `buildx` instead. If you need more control over the process, refer to the [Docker CLI reference for `buildx`][Docker buildx].
| Podman      | 1.16.2+ | Podman also supports `buildx` - but not all of the features from Docker are available. [Podman CLI reference for `build`][Podman build].

:exclamation: From this point forward we will only refer to Podman, but
Docker should support pretty much the same command lines and Dockerfiles.

:exclamation: I prefer to use Debian images, but of course you can use whatever
Linux distribution you want for the base of the container. You may need to
modify some of the `RUN` commands.

:exclamation: I'm assuming that you have `git clone`d this repository and can
navigate to it on your host in the next step. On Windows, you will need to use
the `\` as a path separator.

:exclamation: The command lines assume a Linux or MacOS environment, for Windows
you will need to change the path separator as well as the line continuation
character.

### Starting an Image Build

The simplest way to kick off the build of a new image is:

```
cd path/to/debian-13-slim-base
podman buildx build -f Containerfile -t debian-13-slim-base .

NOTE: Don't forget the trailing "."
```

If you want to avoid changing to the directory where the `Dockerfile`
lives, you can just do this:

```
podman buildx build -t debian-13-slim-base path/to/debian-13-slim-base
```

Depending on network and computer speed, the build time will vary. On my
machine it's about a minute without the cache - and just a few seconds with
the cache.

You can verify that the `Debian 13 (slim)` and our new `debian-13-slim-base`
images exists by running:

```
$ podman image list
REPOSITORY                       TAG         IMAGE ID      CREATED         SIZE
localhost/debian-13-slim-base  latest      cb85902f99a6  57 minutes ago  139 MB
docker.io/library/debian         13-slim     596c6d80c879  8 days ago      81.3 MB
```

### Creating a Container

But that's not quite all there is to it - we still need to create a
container, like this:

```
podman create -it debian-13-slim-base bash
039cb1f886bee4f6cc718982bd81d64967c7437d31cb3412b269df6767e7cbe6
```

And verify that the container exists by running:

```
podman container list --all
CONTAINER ID  IMAGE                                   COMMAND     CREATED             STATUS      PORTS       NAMES
039cb1f886be  localhost/debian-13-slim-base:latest  bash        About a minute ago  Created                 zen_euler
```

### Running a Container

Finally, we can start the container like this, and see if `python3` is
installed and running ...

```
podman start -ai 039cb1
root@039cb1f886be:/# python3
Python 3.13.5 (main, Aug 10 2026, 12:06:59) [GCC 14.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
root@039cb1f886be:/#
```

Now, there are a number of shortcomings with this minimal example, not the least
of which is that we are running as root. So let's get a little fancier and set
things up more securely, and take advantage of mountable disk volumes to keep
our containers well isolated.

## Next Steps - Best Practices for Container Environments


podman buildx build -t debian-13-slim-template     --build-arg USER_NAME=$USER                     devcontainers/debian-13-slim-template
podman create -it   debian-13-slim-template /etc/devcontainer/postStartCommand 
podman start -ai 19



















Now that we have verified a minimal container and image build, we
can add some improvements that make our containers more secure and
support working in containers as if they were our primary computer.

This is especially handy if you don't want to risk messing up your
primary development machine while still having your `ssh` keys and `git`
configuration acessible from the continer.

The first step is to slightly modify the base image by adding
a non-root user that has passwordless `sudo` privileges. Of
course, you can remove `sudo` access once your user has configured
the container.

### Add A non-root User

The first thing we will do is add a non-root user, and install the `sudo`
package. To make this script a bit more general, we have added a number
of build-time arguments that can be overridden on the build command line.

```
ARG USER_NAME=debian
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG USER_LANG=en_US.UTF-8
ARG USER_TZ=Etc/EST
ARG USER_SHELL=/usr/bin/bash
```

The defaults make it so the only thing we need to override on the
command line is our username. Let's build the new image, create
the container, and run it. Note that your container id will be different.

```
podman buildx build -t debian-13-slim-base \
                    -f Containerfile-0-non-root-user \
                    --build-arg USER_NAME=$USER \
                    path/to/debian-13-slim-base
podman create -it debian-13-slim-base bash
podman start -ai 2f42b57bc0

username@2f42b57bc0cc:/$ sudo apt update
```

You will notice that you (or whichever `USER_NAME` you specified) are now
the default user in the running container, and that you have passwordless
`sudo` access. Use it appropriately!

The container starts in the root (`\`) directory, which may not be convenient
but we can change that in a later stage. The remaining customizations are made
at container creation time.


### Renaming the Container

When you create a container, it gets a unique 64 character IDas
well as a more human-readable name, like `blissful-panini`.

You cannot change the ID, but you can give the container whatever
name you want when you create it. That's helpful if you are creating
containers to run on a CI/CD build server and need to have well-known
names so that your CI/CD pipeline commands don't have to change when
you build a new container.


af823bd1c2639834f98d0ba9d6a226a2c62267885b5ec5a5ed447309a0dabf7a
Building a base image from the instructions above will result in
an image with the name `ubuntu-xx.yy-embedded:latest`. The tag
defaults to `latest`. But what if you want
to change that name?

The full name of an image is also called a tag, and you can create as
many tags as you want for an image without using any more disk space.
If you need more control over the tag process, refer to the
[Docker CLI reference for `tag`][Docker tag] or
[Podman CLI reference for `tag`][Podman tag].

You rename/tag an image like this:

```
# Choose podman or docker depending on your containerization tool
#
docker image tag ubuntu-22.04-embedded some-new-name:some-new-tag
podman image tag ubuntu-22.04-embedded some-new-name:some-new-tag
```

Sometimes the orignal tag is a really long string, for example a VSCode
devcontainer has a hash after the name.

`vsc-container-name-614c6be1beb9a2a0db595c65c0d81774b6cd195b6092ff5ca691bd219d5caaa6:latest`

That's not going to be fun, even with copy/paste. So we can substitute
the Image ID for the name, which can be copied from the Docker Desktop
Image tab, or from the command line:

```
docker image list
podman image list

REPOSITORY                      TAG    IMAGE ID     CREATED        SIZE
ubuntu-22.04                    22.04  3b63e27dcd9f 31 minutes ago 2.24GB
vsc-container-name-614c6be1b... latest 047565335b81 16 hours ago   2.25GB
plantuml/plantuml-server        jetty  cba36f940161 6 weeks ago    483MB
...
```

So making that VSCode Image more friendly looks like this:

```
# Choose podman or docker depending on your containerization tool
#
docker image tag 047565335b81 some-new-name:some-new-tag
podman image tag 047565335b81 some-new-name:some-new-tag
```

## `apt` Pinning - Ensure Secure and Repeatable Images

One of the problems we are trying to solve with containers is a repeatable
build environment. This can avoid "it works on my machine" problems and
keeps the development team happy. It also keeps the legacy support team
happy because they can recreate the build environment.

This is true for as long as DockerHub is around, and for as long as
the the Linux distro provides a package manager, and for as long
as package maintainers keep the packages available.

For this reason, it is HIGHLY recommended that your team keeps an
archive of mission critical Docker/Podman images and containers somewhere
safe. For more details on saving images read the
[Docker CLI reference for `image save`][Docker image save]
or the
[Podman CLI reference for `image save`][Podman image save]

The `Dockerfile` is where we specify which packages are to be added
the base Ubuntu image - but how do we ensure that the package versions
stay stable, and still receive security updates? The secret lies
in [`apt` pinning][apt-pinning]

We want to make sure that specific versions of the essential packages
are retreived, but the Ubuntu LTS releases do provide security updates
from time to time. In the past this meant updating the `Dockerfile` with
more specific version strings, but now we encapsulate this in the
`apt.preferences` file that is copied to `/etc/apt` in the image creation
step.

A good example is the `ssh` package, it's at the heart of your container
network access security management. Here is the section from
`apt.preferences` for that package:

```
Package: ssh
Pin: version 1:8.9*
Pin-Priority: 1000
```

This says that version `1:8.9` followed by any additional characters
will be installed. The whole point of the `apt` package manager is
to keep your system up to date. Currently the preferred version of the
`ssh` package for Ubuntu 22.04 (jammy) is:

```
jammy (22.04LTS) (net): secure shell client and server (metapackage)
1:8.9p1-3ubuntu0.10 [security]: all
```

When a security update is made, any old package versions are *deleted* from
the Ubuntu package manager - this makes sense because you don't want to
install a package version with a known security issue.

As long as the Ubuntu Jammy package maintainers keep the version of
`ssh` at `8.9` we are good. Ubuntu 22.04 LTS is by definition the Long Term
Support version, so we can be confident that the version number of `ssh`
is unlikely to change, except for security patches.

## Podman Specific Setup for Windows

There are two relatively simple changes required to be able to use
Podman instead of Docker for your container management.

### VSCode Support for Podman in the Remote Explorer Plugin

The [VSCode Remote Explorer] plugin works together with the
[VSCode DevContainer] plugin to give you visibility into your
container infrastructure - you do not need the [VSCode Docker] plugin
to get this functionality.

The [VSCode DevContainer] plugin assumes that your default container management
tool is Docker. Thanks to the Podman team deciding to use the same command-line
interface as Docker, we can simply set the name of the container management
executable.

Go to Settings -> Dev -> Containers -> DockerPath and set the
field to "podman"

Or, just add this to your `settings.json`:

```
"dev.containers.dockerPath": "podman",
```

Restart VSCode and now your Remote Explorer plugin will call `podman`
to show you all of your container assets, and the DevContiner plugin
will use `podman` to start, stop, and rebuild containers.

### Podman Container -> Host Networking in Windows

CHANGE "path\to\user\.wslconfig":

[wsl2]
autoProxy=false
dnsTunneling=true

ON WINDOWS, container and machine config is here:

C:\Users\HempelRa\AppData\Roaming\containers


The Podman network name resolution works differently than Docker, so
we will need to do some one-time configuration to get around it.

Each Podman machine (there is typically only one) gets a unique IP
address, and you can retreive it from a PowerShell session (your IP
address will be different):

```
Get-NetIpAddress | where { $_.InterfaceAlias -Like '*WSL*' -and $_.AddressFamily -EQ 'IPv4' } | select -ExpandProperty IPAddress
172.17.32.1
```

or from `cmd`:

```
powershell -command "Get-NetIpAddress | where { $_.InterfaceAlias -Like '*WSL*' -and $_.AddressFamily -EQ 'IPv4' } | select -ExpandProperty IPAddress"

```

Now start your Podman machine:

```
wsl --distribution podman-machine-default
```

and edit (using `sudo vi`) the `/etc/containers/containers.conf` file
to add this line in the `[containers]` section. This will allow
`host.containers.internal` to resolve to the IP address that the
host presents to `podman-machine-default` - of course your IP
address will be different.

```
host_containers_internal_ip = "172.17.32.1"
```

It turns out that you can use additional hostnames if you already have
devcontainer files that use a different hostname. For example, in my
devcontainers for embedded developemnt, I run [OpenOCD] and connect
to it from the container using the name `host.gdb.gateway`. So the
`[containers]` section of my `/etc/containers/containers.conf` looks
like this:

```
[containers]
host_containers_internal_ip = "172.17.32.1"
host_docker_internal_ip = "172.17.32.1"
host_gdb_gateway_ip = "172.17.32.1"
```

To translate your IP name to the corresponding variable name in the `[containers]` section, just replace the "." with "_" and add "_ip".

Remember to restart your Podman machine after making any changes:

```
podman machine stop
podman machine start
```

Thanks to [StackOverflow user Anton][StackOverflow Anton] for
[this StackOverflow solution for Podman host networking support][podman host networking].

## Troubleshooting Build Issues

Sometimes the image won't build. Here are a few common failures:

### Failure to Download Packages

We are building on the official Ubuntu images from DockerHub, and in
turn those images will update packages from other servers. Sometimes
those servers are down, in which case trying later helps.

If you are using an externally managed computer, then VPN or other
network settings may be preventing access to certain IP addresses. Consult
your provider for instructions on how to proceed to access external
IP addresses.

For example, you might run into trouble downloading the `plantuml` file
from `github.com`:

```
0.570 Resolving objects.githubusercontent.com ...
0.630 Connecting to objects.githubusercontent.com ...
0.795 ERROR: cannot verify objects.githubusercontent.com's certificate ...
0.795   Unable to locally verify the issuer's authority.
0.795 To connect to objects.githubusercontent.com insecurely, use `--no-check-certificate'.                             -
```

Yeah, don't start modifying the `Dockerfile` - the problem is most likely
your network settings. In my case I just had to (temporarliy) disable the
`ZScaler` Internet Security setting on my managed laptop. Note that it
was still on the VPN and that our organization sets a timeout so that
if you forget to turn it back on you are still safe.

### Cache Confusion

Having a cache of previously created container layers really helps to
speed up container construction - but sometimes the cache works against
you. One way around this is to force a build without the cache:

```
# Choose podman or docker depending on your containerization tool
#
docker buildx build --no-cache -t ubuntu-xx.yy-embedded path/to/ubuntu-xx.yy-embedded-docker
podman buildx build --no-cache -t ubuntu-xx.yy-embedded path/to/ubuntu-xx.yy-embedded-docker
```

As an absolute last resort, you can consider clearing out your entire
Docker cache - this can actually free up quite a bit of disk space, but you
will slow down any subsequent container builds until the cache is refilled.

```
docker buildx prune -f
```

Podman users will need to manage unused images, containers, and volumes either
with the GUI or command lines.


:exclamation: If you are using Podman, then you will need to make a
few adjustments to be able to use the VSCode Docker support plugin and to
connect from the container to a network port on the host machine. This
is described in [Podman Specific Setup for Windows](#Podman-Specific-Setup-for-Windows)
near the end of this document.







## More Detailed Information

Managing users in rootless mode
https://medium.com/@guillem.riera/making-visual-studio-code-devcontainer-work-properly-on-rootless-podman-8d9ddc368b30

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
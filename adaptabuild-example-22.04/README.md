## What is `adaptabuild`?

The `adaptabuild` system is really three components that work together
to make setting up an Embedded Systems Devlopment environment much less
complex, no matter which OS your host computer runs - Linux, Windows,
or MacOS.

The three components are:

1. A Docker image (~2.2 GB) based on Ubuntu:22.04-LTS that has everything
   needed to develop, test, debug, and document an ARM Cortex project
   from the Linux command line.

2. A VSCode Devcontainer that is build from the Docker image that has
   all the plugins needed to develop, test, debug, and document an ARM
   Cortex project. That means VSCode *is* the IDE - you can single
   step your code, look at MCU registers, read/write memory, etc.

3. An optional build system based on `make` that lets you focus on
   your project, not learn yet another new and more complex build
   system. You can still choose to use `cmake`, `meson`, `Zephyr` or
   any other tools to build your project.

You and your team can work in a standard environment - no
more wasting time figuring out why the build fails on Evan's machine
and works on Rebecca's.

When you check your work in to `git`, the *same* Docker base image
can be used to build your project using whatever pipeline manager your
CI system uses.

The source for the Docker image and VSCode devcontainer are freely available
so you can tune the contents if necessary. "Infrastructure as code" is one
of the North Star design goals for this project. Nobody wants to spend time
hand-tweaking development environments.

This guide assumes that you are either already an embedded systems
developer, or a learner that has at least some programming experience
with an IDE. This is not a step-by-step guide for learning embedded
systems programming, or a tutorial on how to use the debugger in
VSCode, or how to use Docker.

There are two reasons for this. First, any instructions or screenshots
can become outdated quickly, so I'm pointing at official install pages
for third party code. Second, it's very difficult to make a guide that
is both broad enough and deep enough - so I'm shooting for the middle and
assuming that you have the ability to fill in the gaps.

If you are willing to invest about 30 minutes in trying `adaptabuild` I would
be happy to have any feedback on potential improvements or success stories
you are able to share. Open an issue on this project page and I'll do
my best to answer.

## Installation

You will need to perform 4 tasks to get started:

1. Install the prerequisite software packages (Docker Desktop, VSCode, git)
1. Clone one `git` repository containing the Docker base image creator and 
   the Devcontainer creator
2. Build the Docker base image (one command line and a 5-10 minute wait)
3. Build the VSCode Devcontainer (open a folder and a 3-5 minute wait)

Once that's done, the devcontainer post-build script will automagically
clone *this* repository and you will be ready to debug an example program.

### Install Prerequisite Software

NOTE: Users behind a corporate firewall *may* need to temporarily turn
off the firewall to complete the setup of the Docker base image and
the VSCode devcontainer. 

No matter which operating system you do your work on, you will need to
have the following programs installed on your system. I won't go into the
install details - please follow the directions on the install page for
each product.

### Docker

Follow the links below to the official Docker Desktop installation guide for
your operating system. Stick with any defaults the installer offers.

- [Install Docker Desktop for Windows][Docker Install Windows]
- [Install Docker Desktop for MacOS][Docker Install MacOS]
  
Linux users should install the `docker` package for your distro. Using
Docker Desktop on Linux actually adds *another* Linux VM instead of
using the underlying support that your Linux machine already gives you.

If you insist on using Docker Desktop on Linux ...

- [Install Docker Dektop for Linux][Docker Install Linux] - Read the Important Info!

### Microsoft VSCode

Follow the links below to the offical Microsoft VSCode installation guide
for your operating system. Stick with any defaults the installer offers.

- [Install VSCode for Windows, MacOS, Linux][Install VSCode]
- [Install the official Docker plugin for VSCode][Install Docker Plugin]

You don't need to install any additional VSCode plugins on your host operating
system - the `.devcontainer` file will install them *in the container* without
changing your host VSCode setup.

### `git`

Follow the links below to the official `git` installation guide for
your operating system. Stick with any defaults the installer offers.

- [Install Docker Desktop for Windows][Docker Install Windows]
- [Install Docker Desktop for MacOS][Docker Install MacOS]
  
Linux users should install the `git` package for your distro - it's
probbaly alerady installed.

### Clone the `git` Repositories

Using the git command line (or whatever GUI you choose), clone the following
repositories wherever you do your work:




 Using
Docker Desktop on Linux actually adds *another* Linux VM instead of
using the underlying support that your Linux machine already gives you.


   from Microsoft. You don't need to install any additional plugins - the
   `.devcontainer` file will install them *in the container* without changing
    your host VSCode setup.
1. `git clone` this repository to some place convenient.
[Install VSCode]: https://code.visualstudio.com/download

. Install VSCode on your Windows, MacOS, or Linux machine
   [from the official site](https://code.visualstudio.com/).
   Make sure that you check the dialog box for these options during setup:
   - Add "Open with code” action to Windows Explorer file context menu
   - Add “Open with code” action to Windows Explorer directory context menu
   MacoS and Linux users may have similar options during the install process in the setup wizard. If you forget this step then the right click and "Open with code"
   will not work. You can re-install at any time to enable the options.
1. Install the
   [official `Docker` plugin for VSCode](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
   from Microsoft. You don't need to install any additional plugins - the
   `.devcontainer` file will install them *in the container* without changing
    your host VSCode setup.
2. `git clone` this repository to some place convenient.

With those prerequisites in place, it's time to build the container:

1. Make sure the Docker daemon is running. Windows and MacOS users may
   need to click the DockerDesktop icon. Some installs may automatically
   start DockerDesktop when you log in to your computer.
2. In the Windows (or MacOS or Linux) desktop (not from within VSCode), navigate
   to where you cloned this repository, then right click on the
    `lcra-test-devcontainer` folder and choose *Open with VSCode*.
3. VSCode may recognize the .devcontainer folder and begin building the
   container. If not, you can start the build manually using `Ctrl-Shift-P` to
   open up a list of commands, and then type `Rebuild Container`
   to start the build process. This usually takes less than 5 minutes.
4. If the build fails, you may need to *temporarily* disable your
   firewall. Either retry or repeat step 3.
5. In some extreme situations, you may need to rebuild the container completely
   from scratch. `Ctrl-Shift-P` to open up a list of commands, and then
   type `Rebuild Container Without Cache`

Once that is done, you will have a container running Ubuntu 22.04 that has
all the tools need to develop the `lcra-test` tool.

## Common Problems

### `.ssh` Credential Permissions

The `.devcontainer` file defines how the Docker container is integrated with
VSCode. To make the experience as seamless as possible, we mount your `$HOME\.ssh`
folder in the container at `~/.ssh` automatically. This saves you the step of copying your
credentials all over the place.

However, the Linux `ssh` system is picky about file permisisons on your `~/.ssh`
and helpfully does nothing and gives you a warning if they are set up insecurely.

If the clone of the `lcra-test` repo fails, check your permissions once it is
mounted. They should look like this:

```
lcra@7e96091a1815:~/projects/lcra-test$ ls -al ~/.ssh
total 32
drwx------ 1 lcra lcra  512 Jun 27 14:50 .
drwxrwxrwx 1 root root  512 Jun 28 12:52 ..
-rw------- 1 lcra lcra 1727 Nov 22  2023 config
-rw------- 1 lcra lcra 3381 May 31  2023 fireapp_id_rsa
-rw-r--r-- 1 lcra lcra  744 May 31  2023 fireapp_id_rsa.pub
-rw------- 1 lcra root  399 Oct 30  2023 gitlab-runner
-rw-r--r-- 1 lcra root   96 Oct 30  2023 gitlab-runner.pub
-rw------- 1 lcra root  399 May 15 16:57 id_xxx
-rw-r--r-- 1 lcra root   94 May 15 16:57 id_xxx.pub
-rw------- 1 lcra root 1679 Jan  8  2017 id_rsa.xxx
-rw-r--r-- 1 lcra root  398 May 29  2014 id_rsa.xxx.pub
-rw------- 1 lcra root 5755 May 29 15:49 known_hosts
-rw------- 1 lcra lcra 4236 Sep 12  2023 known_hosts.old
```

- The `.ssh` directory is owned by the `lcra` user
- The `.ssh` directory is only accessible to the owner `700 drwx------`
- All the files are read/write for the owner `600 -rw-------`
- All the `.pub` files are readable by everyone `644 -rw-r--r--`

You can run these commands to get things right if needed:

```
cd ~
sudo chown -R lcra .ssh
chmod 700 ~/.ssh
chmod 600 ~/.ssh/*
chmod 644 ~/.ssh/*.pub
```

### `.ssh/known-hosts` Contents

If you have never connected to the [Edwards Gitlab](http://vbsa003.carcgl.com:81/)
instance before, chances are that your `.ssh\known_hosts` file will not have
a line for that server, and any `git` operations will either fail, or will prompt
for you to add the server to the `.ssh\known_hosts` file.

Of course, cloning this repo should automagically add the Edwards Gitlab host
to your `.ssh\known_hosts` file.




[Docker Install Windows]: https://docs.docker.com/desktop/install/windows-install/
[Docker Install MacOS]: https://docs.docker.com/desktop/install/mac-install/
[Docker Install Linux]: https://docs.docker.com/desktop/install/linux-install/
[Install VSCode]: https://code.visualstudio.com/download
[Install Docker Plugin]: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker]

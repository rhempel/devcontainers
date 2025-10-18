IMPORTANT NOTE
--------------

Container environments can fail in mysterious ways - logs are your friend.

On Windows, the VSCode devcontainer logs are stored at:

`C:\Users\your_userid\AppData\Roaming\Code\logs`

You can access them from the VSCOde session with the command:

`Devcontainers Developer : Show All Logs`

HOME vs USER Environment Variable under Windows
-----------------------------------------------

Very frequently, my containers would fail to start because some of
the command scripts that are executed as part of the container 
create/start/connect cycle fail.

The issue was that my managed Windows system has inconsistent values
for some critical environment variables. Looking throuhg the logs we
can see that the Windows environment variables include:

```
"USERNAME":"hempelra"
"USERPROFILE":"C:\\Users\\HempelRa"
```

The user that the container system sees, is:

```
"user":"HempelRa"
```

Why is this a problem? The postCreate step sets up your user's home directory
in the container with the "user" environment variable. In my case it will be
at:

`mkdir -p '/home/HempelRa/.devcontainer'`

But when we actually run the postStart.sh script, the `USERNAME` string is
used, resulting in:

`/bin/sh -c bash ./.devcontainer/commands/postStartCommand.sh hempelra`

To make things worse, when we expand $HOME inside that script, we end up
at:

`/home/hempelra` - which doesn't exist.

We can do a couple of things:

1. In the postCreate.sh script, create a soft link so that no matter what
   the `USERNAME` is, accessing HOME evaluates to `/home/HempelRa/`. The
   disadvantage with this approach is that it involves working around the
   problem with a fragile solution that doesn't always work.

2. Find a way to force the value in `user` rather than `USERNAME` when
   running the postCreate/postStart/postCOnnect scripts.

There are too many places where the `user` value is embedded in commands
and paths that we have no control over.




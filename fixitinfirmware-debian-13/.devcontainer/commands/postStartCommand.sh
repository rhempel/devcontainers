# Put the current user into an environment variable. Containers
# run with the login user "root" running as whatever the USER varaible
# is set to in the Dockerfile
#
export WHOAMI=$(whoami)

cd ~

# The .ssh folder is mounted as an overlay, so any changes here
# don't affect the host system, and changes on the host system 
# are invisible until the next time the container is restarted.
#
# Now set the correct ownership to the entire .ssh folder
# and then set the correct permissions for the contents
#
sudo chown -R $WHOAMI:$WHOAMI .ssh

chmod 700 .ssh
chmod 600 .ssh/*
chmod 644 .ssh/*.pub

# Create the authorized_keys file , then append the keys that
# you want to authorize for this container.
#
(umask 177 && touch -c .ssh/authorized_keys)
cat .ssh/id_hempelra.pub >> .ssh/authorized_keys

# Now update the ssh_config.d folder with a file that will allow
# our user to access the container over ssh
#
sudo sh -c "echo 'AllowUsers $WHOAMI' > /etc/ssh/sshd_config.d/30-userlist.conf"
sudo /etc/init.d/ssh restart

# The container's .gitconfig is mounted under ~/.devcontainer
# Make # any machine specific changes as --local or --global here
#
cp ~/.devcontainer/files/.gitconfig ~/.gitconfig

 # Update the .gitconfig file by combining the original .gitconfig
# # created when the devcontainer was created with the current
# # users's .gitconfig that was mounted at ~/.gitconfig.host
# #
# cd ~
# 
# if [ ! -f .gitconfig.original ]; then
#   echo "copying .gitconfig" >> ~/postStart
#   cp .gitconfig .gitconfig.original
# fi;
# 
# if [ ! -f .gitconfig ]; then
#   echo "No .gitconfig" >> ~/postStart
#   cp .gitconfig .gitconfig.original
# fi;
# 
# # Now create the updated .gitconfig
# #
# cat .gitconfig.original .gitconfig.host > .gitconfig

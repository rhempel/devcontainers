this_user=$1

sudo chown "$this_user" /home/"$this_user"/projects
sudo ln -sf /usr/bin/python3 /usr/bin/python

echo "==============================================================="
echo user is $1
echo HOME is $HOME
sleep 5

# Assume that worked and fetch (don't pull!) and updates
#
cd ~/projects

if [ -d adaptabuild-example ]; then
  cd adaptabuild-example
  git fetch --recurse-submodules
fi;

this_user=$1

# Check for and clone the adaptabuild-example if it doesn't exist
#
cd ~/projects

if [ ! -d adaptabuild-example ]; then
  git clone https://github.com/rhempel/adaptabuild-example.git
  cd adaptabuild-example
  git submodule update --init --recursive
fi;

# The section on custom gitconfig should be handled with an include see
# the container_base_images repo for notes

# # Update the .gitconfig file by combining the original .gitconfig
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

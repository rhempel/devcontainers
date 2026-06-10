this_user=$1

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

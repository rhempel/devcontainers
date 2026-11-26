#!/bin/bash
# -----------------------------------------------------------------------------
# create_container.sh - Builds a container image
#
# This script must be executed (not sourced) to avoid polluting the namespace
# of the calling shell ...
#
(return 0 2>/dev/null) && is_sourced=1 || is_sourced=0

if [ $is_sourced -ne 0 ]; then
  echo "$(basename ${BASH_SOURCE[0]}) must be executed, not sourced"
  unset is_sourced
  return 1
fi

show_help () {
cat << EOF
Usage: ${0##*/} [options]

Create a container instance according to a configuration file.

  -c|--config CONFIG  Configuration to use - default is "default"
  -r|--replace        Replace the container instance if one already exists
  -h|--help|\-?       Show this help text and exit
  --test)             Dry run - print the generated podman command line
EOF
}

create_container_test_run=""

run () {
    if [ "${create_container_test_run}" ]; then
      echo "create_container: $*"
    else 
      eval "$@"
    fi
}

# -----------------------------------------------------------------------------
# create_container_options prefix map
#
create_container_options () {
  local prefix=$1
  local -n map=$2

  for item in "${map[@]}" ; do
    options+=" --${prefix} $item"
  done
  echo $options
}

create_container () {
  source $(dirname ${BASH_SOURCE[0]})/../../configs/"${create_container_config_file}"

  container_user="${container_user}"
  container_image="${container_basename}":"${container_tagname}"
  container_name="${container_basename}"-"${container_tagname}"
  container_config="${container_tagname}"

  container_hosts=$(create_container_options "add-host" create_container_host_maps)
  container_volumes=$(create_container_options "volume" create_container_volume_maps)
  container_publish=$(create_container_options "publish" create_container_port_maps)

  run podman create -it "${create_container_replace}" \
                        --name="${container_name}" \
                        "${container_hosts}" \
                        "${container_volumes}" \
                        "${container_publish}" \
                        "${container_image}" \
                        /etc/devcontainer/postStartCommand 
}

main () {
  while [[ "$#" -gt 0 ]]; do
    case $1 in
      -c|--config)   create_container_config_file="$2"; shift ;;
      -r|--replace)  create_container_replace="--replace" ;;
      -h|--help|-\?) show_help; return 0 ;;
      --test)        create_container_test_run="y" ;;
      *)             echo "Unknown parameter passed: $1"; return 1 ;;
    esac
    shift
  done
}

if main "$@"; then
  create_container
fi

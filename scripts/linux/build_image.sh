#!/bin/bash
# -----------------------------------------------------------------------------
# build_image.sh - Builds a container image
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

Build a customized container image that can be used to create a container
instance.

  -c|--config CONFIG  Configuration to use
  -h|--help|\-?       Show this help text and exit
  --test              Dry run - print the generated podman command line
EOF
}

build_image_test_run=""

run () {
    if [ "${build_image_test_run}" ]; then
      echo "build_image: $*"
    else 
      eval "$@"
    fi
}

build_image () {
  source $(dirname ${BASH_SOURCE[0]})/../../configs/"${build_image_config_file}"

  build_image_user="${container_user}"
  build_image_tag="${container_basename}":"${container_tagname}"
  build_image_template="${container_basename}"
  build_image_config="${container_tagname}"

  run podman buildx build -t "${build_image_tag}" \
                          --build-arg USER_NAME=${build_image_user} \
                          --build-arg CONTAINER_CONFIG=${build_image_config} \
                          devcontainers/templates/"${build_image_template}"
}

main () {
  while [[ "$#" -gt 0 ]]; do
    case $1 in
      -c|--config)   build_image_config_file="$2"; shift ;;
      -h|--help|-\?) show_help; return 0 ;;
      --test)        build_image_test_run="y" ;;
      *)             echo "Unknown parameter passed: $1"; return 1 ;;
    esac
    shift
  done
}

if main "$@"; then
  build_image
fi

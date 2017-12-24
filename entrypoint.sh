#!/usr/bin/env bash

set -e

if [[ ("$1" = "ipwb") && ("$1" != "$@") && ("$@" != *" -h"*) && ("$@" != *" --help"*) ]]
then
    # Initialize IPFS if not initialized already
    if [ ! -f $IPFS_PATH/config ]
    then
        ipfs init
    fi
    # Run the IPFS daemon in background
    ipfs daemon &

    # Wait for IPFS daemon to be ready
    while ! curl -s localhost:5001 > /dev/null
    do
        sleep 1
    done
fi

exec "$@"

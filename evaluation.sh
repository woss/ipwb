#!/bin/bash

function cleanIPFS {
  rm -rf ~/.ipfs
  ipfs init
  rm /tmp/xxx
}
function runSizeMessage {
  echo "Running size(msg)"
  cleanIPFS
  
  SECONDS=0
  ipfs daemon &
  ipwb index mkelly2.warc
  #echo $!
  kill -SIGKILL $!

  echo "$SECONDS second(s) elapsed"

  du -hcs ~/.ipfs | tail -1
}

function runSizeEncryptMessage {
  echo "Running size(encrypt(msg))"
  cleanIPFS
  
  SECONDS=0
  ipfs daemon &
  ipwb index -e mkelly2.warc
  kill -SIGKILL $!

  echo "$SECONDS second(s) elapsed"

  du -hcs ~/.ipfs | tail -1
}


ipwb --version
runSizeMessage
#runSizeCompressMessage

runSizeEncryptMessage

#export IPFS_PATH=/path/to/ipfsrepo
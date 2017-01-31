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
  ipwb index mkelly2.warc > /tmp/xxx
  echo $!
  #kill -SIGKILL $!

  echo "$SECONDS second(s) elapsed"

  du -hcs ~/.ipfs | tail -1
}

function runSizeEncryptMessage {
  echo "Running size(compress(msg))"
  cleanIPFS
  
  SECONDS=0
  ipfs daemon &
  ipwb index -e mkelly2.warc > /tmp/xxx
  kill -SIGKILL $!

  echo "$SECONDS second(s) elapsed"

  du -hcs ~/.ipfs | tail -1
}


ipwb --version
runSizeMessage
#runSizeCompressMessage

#runSizeEncryptMessage
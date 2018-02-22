#!/bin/bash

# start sshd and fall into bash
/etc/init.d/ssh start
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start sshd: $status"
  exit $status
fi

/bin/bash

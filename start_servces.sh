#!/bin/bash

# start sshd and fall into bash
/etc/init.d/ssh start
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start my_second_process: $status"
  exit $status
fi

/bin/bash

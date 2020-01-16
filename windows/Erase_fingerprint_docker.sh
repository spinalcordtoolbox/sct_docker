#!/bin/bash
#
grep -v "192.168.99.100" ~/.ssh/known_hosts | grep -v "localhost" > ~/.ssh/known_hosts.txt
cat ~/.ssh/known_hosts.txt > ~/.ssh/known_hosts
rm ~/.ssh/known_hosts.txt

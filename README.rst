.. -*- coding: utf-8; indent-tabs-mode:nil; -*-


##########################
Spinal Cord Toolbox Docker
##########################


Docker for Windows
##################


Usage
*****

#. Start container

   .. code:: sh

      docker run -p 2222:22 --rm -it sct-official-3.1.1

#. Connect to it: run ``windows/sct-win.xlaunch``.



Offline Installation
********************

#. Install git (in case you don't already have it), this is to provide
   an ssh binary.

#. Install Xming.

#. Install Docker.

#. Open PowerShell and run:

   .. code:: sh

      docker load sct-official-3.1.1.tar


Construction
************

.. code:: sh


An SCT  with ssh Dockerfile
To build the container:
docker build --tag neuropoly/sct .

To run the sct:

Then ssh to the contaner with X tunelling enable  option and the port to 2222 on the local host , you should then be
able to all sct features on a windows machine.





Offline Archives
################

Usage
*****

#. Extract archive:

   .. code:: sh

      cd $HOME
      tar xzf /path/to/offline-archive-sct-ubuntu_16_04-sct3.1.1.tar.gz


#. Add PATH:

   .. code:: sh

      PATH+=":$HOME/sct_3.1.1/bin"

#. Use it!

   .. code:: sh

      sct_check_dependencies


Generation
**********

Supported distributions:

.. code:: sh

   distros="debian:7 debian:8 debian:9 ubuntu:14.04 ubuntu:16.04 ubuntu:18.04 fedora:27"
   version="3.1.1"
   install_folder="sct_$version"


Creation of container images:

.. code:: sh

   > containers.lst
   for distro in $distros; do
     ./sct_docker.py generate --distro $distro >> containers.lst
   done

   containers=$(< containers.lst)
   for container in $containers; do
    docker build -t $container $container; \
   done

Example of distribution:

.. code:: sh

   for container in $containers; do
     docker tag $container zougloub/neuropoly:$container;
     docker push zougloub/neuropoly:$container;
   done

Creation of offline archives:

.. code:: sh

   containers=$(< containers.lst)
   for container in $containers; do
     docker run "$container" tar --create $install_folder \
      | gzip \
      > offline-archive-${container}.tar.gz
   done





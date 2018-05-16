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

#. Extract archive in `/home/sct` (unfortunately due to hard-coded paths in the
installation folder, this is mandatory):

   .. code:: sh

      cd $HOME
      tar xf /path/to/sct-sct3.1.1-ubuntu_16_04-offline.tar.xz

#. Add PATH:

   .. code:: sh

      PATH+=":/home/sct/sct_3.1.1/bin"

#. Use it!

   .. code:: sh

      sct_check_dependencies


Generation and Distribution
***************************

The tool `sct_docker_images.py` helps with creation and distribution
of SCT Docker images.

Example: creation of container images:

.. code:: sh

   ./sct_docker_images.py generate

Example: creation of offline archive tarball:

.. code:: sh

   ./sct_docker_images.py generate --generate-offline-sct-distro

Example: creation and distribution:

.. code:: sh

   ./sct_docker_images.py generate --publish-under zougloub/neuropoly

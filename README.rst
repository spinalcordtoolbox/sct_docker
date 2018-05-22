.. -*- coding: utf-8; indent-tabs-mode:nil; -*-


##########################
Spinal Cord Toolbox Docker
##########################


.. contents::
..
    1  Docker for Windows
      1.1  Usage
      1.2  Online Installation
      1.3  Offline Installation
    2  Docker for Other OSes
      2.1  Usage
      2.2  Online Installation
      2.3  Offline Installation
    3  Offline Archives
      3.1  Usage
    4  Generation and Distribution


Docker for Windows
##################


That would be the main reason to use Docker, as SCT can be installed
pretty much anywhere else.


Usage
*****

#. Start throw-away container on the image:

   .. code:: sh

      docker run -p 2222:22 --rm -it sct-3.1.1-official

#. Change the password (default is `sct`) from the container prompt:

   .. code:: sh

      passwd

#. Connect to it using Xming/SSH if X forwarding is needed
   (eg. running FSLeyes from there):

   Run ``windows/sct-win.xlaunch`` found in this repository.


Notes:

- Read the Docker documentation to create a persistent container
  from the image, map your local folders on the container, which you
  probably want to perform.


Online Installation
*******************


#. Install git (in case you don't already have it), this is to provide
   an ssh binary.

#. Install Xming.

#. Install Docker (or Docker Toolbox on Windows Home).

#. Fetch the SCT image from `Docker Hub <https://hub.docker.com/r/neuropoly/sct/>`_:

   Open PowerShell and run:


   .. code:: sh

      docker pull neuropoly/sct:sct-3.1.1-official


Offline Installation
********************

#. Install git (in case you don't already have it), this is to provide
   an ssh binary.

#. Install Xming.

#. Install Docker (or Docker Toolbox on Windows Home).

#. Load the SCT image from a local file

   Open PowerShell and run:

   .. code:: sh

      docker load sct-3.1.1-official.tar



Docker for Other OSes
#####################


Usage
*****

#. Start throw-away container on the image:

   .. code:: sh

      docker run -p 2222:22 --rm --tty --interactive sct-3.1.1-official


#. Change the password (default is `sct`) from the container prompt:

   .. code:: sh

      passwd

#. Connect to container using SSH if X forwarding is needed
   (eg. running FSLeyes from there):

   .. code:: sh

      ssh -Y sct@localhost:2222


Notes:

- Read the Docker documentation to create a persistent container
  from the image, map your local folders on the container, which you
  probably want to perform.


Online Installation
*******************

#. Install Docker

#. Fetch the SCT image from `Docker Hub <https://hub.docker.com/r/neuropoly/sct/>`_:

   .. code:: sh

      docker pull neuropoly/sct:sct-3.1.1-official


Offline Installation
********************

#. Install Docker.

#. Load the SCT image from a local file

   .. code:: sh

      docker load sct-3.1.1-official.tar



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
###########################

The tool `sct_docker_images.py` helps with creation and distribution
of SCT Docker images.

Example: creation of container images:

.. code:: sh

   ./sct_docker_images.py generate --version 3.1.1

Example: creation of offline archive tarball:

.. code:: sh

   ./sct_docker_images.py generate --version 3.1.1 --generate-offline-sct-distro

Example: creation and distribution:

.. code:: sh

   ./sct_docker_images.py generate --version 3.1.1 --publish-under neuropoly/sct



General Notes
#############

- Caveat #1: When building images, specify a tag name or commit id, not a branch
  name, unless you have invalidated the Docker cache... or Docker will
  reuse whatever was existing and not test the right version


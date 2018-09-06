.. -*- coding: utf-8; indent-tabs-mode:nil; -*-


##########################
Spinal Cord Toolbox Docker
##########################

In this documentation file is used the SCT version 3.2.1 in the examples, if you want
install a different version of SCT please change the 3.2.1 by the version number you want.

.. contents::
..
    1  Docker for Windows
      1.1  Online Installation
      1.2  Offline Installation
      1.3  Usage
    2  Docker for Other OSes
      2.1  Online Installation
      2.2  Offline Installation
      2.3  Usage
    3  Offline Archives
      3.1  Usage
    4  Generation and Distribution
    5  General Notes
    6  Support


Docker for Windows
##################

That would be the main reason to use Docker, as SCT can be installed directly pretty much anywhere else.

Note: in case of problem, see `Support`_.

Docker runs natively only on Windows 10 Pro/Enterprise. Download the docker installer from the `Docker official site <https://store.docker.com/editions/community/docker-ce-desktop-windows/>`_

To Install Docker in Windows XP/VISTA/7/8/8.1/10 others than Pro/Enterprise use `Docker Toolbox <https://docs.docker.com/toolbox/overview/>`_. Here is the the `tutorial <https://docs.docker.com/toolbox/toolbox_install_windows/>`_.

When using Docker Toolbox, mounting folders in a docker container can be a bit complicated and has certain limitations.
The main limitation is that by default we will only be able to mount folders that are inside the C:/Users folder.


To be able to process NIFTI volumes that we have in our Windows PC we will go to the folder ``C:/Users`` and create a folder called ``docker_shared_folder`` This folder that we have just created will be our work folder in which we will place all the volumes that we want to process using the SCT.



Online Installation
*******************


#. Install git (in case you don't already have it), this is to provide
   an ssh binary.

#. Install `Xming <https://sourceforge.net/projects/xming/files/Xming/6.9.0.31/>`_.

#. Install Docker (or Docker Toolbox depending of your Windows version).

#. Fetch the SCT image from `Docker Hub <https://hub.docker.com/r/neuropoly/sct/>`_:

   Open CMD or if you are using Docker Toolbox open Docker Quickstart Terminal wait until get a prompt and run:


   .. code:: sh

      docker pull neuropoly/sct:sct-3.2.1-official

#. If you are **NOT** using Docker Toolbox skip this step. To avoid memory issues when running the SCT is important to increment the default amount of RAM (1GB) of the Docker VM. To do this:

   Open Docker Quickstart Terminal wait until get a prompt and run:

   .. code:: sh

      docker-machine stop default

      /c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe modifyvm default --memory 2048

      docker-machine start default

   **Note:** With these commands we have increased the RAM memory of the VM Docker to 2GB. It is important that your PC have at least 3 GB of RAM in order to leave at least 1 GB for your Windows host system.



#. Go to C:/Users and create the folder named ``docker_shared_folder``



Offline Installation
********************

#. Install git (in case you don't already have it), this is to provide
   an ssh binary.

#. Install `Xming <https://sourceforge.net/projects/xming/files/Xming/6.9.0.31/>`_.

#. Install Docker (or Docker Toolbox depending of your Windows version).

#. Load the SCT image from a local file

   Open CMD or if you are using Docker Toolbox open Docker Quickstart Terminal wait until get a prompt and run:

   .. code:: sh

      docker load --input sct-3.2.1-official-ubuntu_18.04.tar

  **Note:** After the --input parameter you can include the complete path where the docker image is located. In the example it is assumed that the image is in the current directory

#. If you are **NOT** using Docker Toolbox skip this step. To avoid memory issues when running the SCT is important to increment the default amount of RAM (1GB) of the Docker VM. To do this:

   Open Docker Quickstart Terminal wait until get a prompt and run:

   .. code:: sh

      docker-machine stop default

      /c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe modifyvm default --memory 2048

      docker-machine start default

   **Note:** With these commands we have increased the RAM memory of the VM Docker to 2GB. It is important that your PC have at least 3 GB of RAM in order to leave at least 1 GB for your Windows host system.


#. Go to ``C:/Users``and create the folder named ``docker_shared_folder``


Usage
*****

#. Start throw-away container on the image. If you are using Docker toolbox open Docker Quickstart Terminal wait until get a prompt and write:

   .. code:: sh

      docker run -p 2222:22 --rm -it -v //c/Users/docker_shared_folder://home/sct/docker_shared_folder sct-3.2.1-ubuntu-18.04

   **Note:** The folder ``C:/Users/docker_shared_folder`` on the Windows host system will be linked to the folder ``/home/sct/docker_shared_folder`` inside the Docker container and the changes made to it will be visible for both the Docker container and the Windows system.

#. (NOT MANDATORY) Change the password (default is `sct`) from the container prompt:

   .. code:: sh

      passwd

#. Connect to it using Xming/SSH if X forwarding is needed
   (eg. running FSLeyes from there):

   Run (double click) ``windows/sct-win.xlaunch`` found in this repository. If you are using docker toolbox then then run``windows/sct-win_docker_toolbox.xlaunch``

#. If this is the first time you have done this procedure, the system will ask you if you want to add the remote PC (the docker container) as trust pc, type "yes" without "". Then type the password to enter the docker container (by default "sct" without "").

#. The graphic terminal emulator LXterminal should appear, which allows copying and pasting commands, which makes it easier for users to use it. To check that X forwarding is working well write fsleyes & in LXterminal and FSLeyes should open, depending on how powerful your computer is FSLeyes may take a few seconds to open.

#. If after closing a program with graphical interface (i.e. FSLeyes) LXterminal does not raise the Liniux ($) prompt then press Ctrl + C to finish closing the program.

#. Then enjoy SCT ;)


Docker for Unix like OSes (GNU/Linux, BSD family, MacOS)
########################################################

Online Installation
*******************

#. Install Docker

#. Fetch the SCT image from `Docker Hub <https://hub.docker.com/r/neuropoly/sct/>`_:

   .. code:: sh

      docker pull neuropoly/sct:sct-3.2.1-official


Offline Installation
********************

#. Install Docker.

#. Load the SCT image from a local file

   .. code:: sh

      docker load --input sct-3.2.1-official-ubuntu_18.04.tar


Usage
*****

#. Create a folder called ``docker_shared_folder`` in your home directory to be able to share information between your host system a the docker container.

   .. code:: sh

      mkdir ~/docker_shared_folder

#. Start throw-away container on the image:

   .. code:: sh

      docker run -p 2222:22 --rm -it -v ~/docker_shared_folder://home/sct/docker_shared_folder neuropoly/sct:sct-3.2.1-official


#. (NOT MANDATORY) Change the password (default is `sct`) from the container prompt:

   .. code:: sh

      passwd

#. Connect to container using SSH if X forwarding is needed
   (eg. running FSLeyes from there):

   .. code:: sh

      ssh -Y sct@localhost:2222

#. Then enjoy SCT ;)


Offline Archives
################

Usage
*****

#. Extract archive in `/home/sct` (unfortunately due to hard-coded paths in the
   installation folder, this is mandatory):

   .. code:: sh

      cd $HOME
      tar xf /path/to/sct-sct3.2.1-ubuntu_18_04-offline.tar.xz

#. Add PATH:

   .. code:: sh

      PATH+=":/home/sct/sct_3.2.1/bin"

#. Use it!

   .. code:: sh

      sct_check_dependencies




Generation and Distribution
###########################

The tool `sct_docker_images.py` helps with creation and distribution
of SCT Docker images.

List of suported distros for docker images:

- ubuntu:14.04
- ubuntu:16.04
- ubuntu:18.04
- debian:8
- debian:9
- fedora:25
- fedora:26
- fedora:27
- fedora:28
- centos:7

For the official image that is released on docker hub we use the Ubuntu 18.04 based image

Example: creation of all distros container images:

.. code:: sh

   ./sct_docker_images.py generate --version 3.2.1

Example: creation of offline archive tarball:

.. code:: sh

   ./sct_docker_images.py generate --version 3.2.1 --distros ubuntu:18.04 --generate-distro-specific-sct-tarbal

Example: creation and distribution:

.. code:: sh

   ./sct_docker_images.py generate --version 3.2.1 --publish-under neuropoly/sct


General Notes
#############

- Caveat #1: When building images, specify a tag name or commit id, not a branch
  name, unless you have invalidated the Docker cache... or Docker will
  reuse whatever was existing and not test the right version


Support
#######

Please try to differentiate issues about the SCT Docker packages or
tools, and SCT itself.

In case of problem, create issues `on the github project
<https://github.com/neuropoly/sct_docker/issues>`_ and provide information
allowing to quickly assist you.

Thank you!

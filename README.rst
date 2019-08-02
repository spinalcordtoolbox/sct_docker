.. -*- coding: utf-8; indent-tabs-mode:nil; -*-

##########################
Spinal Cord Toolbox Docker
##########################

This documentation shows how to install the latest version of SCT. If you want install a different version of SCT please specify the version number you want.

.. contents::
..
    1  Docker for Windows
      1.1  Installation
      1.2  Usage
    2  Docker for Unix like OSes (GNU/Linux, BSD family, MacOS)
      2.1  Installation
      2.2  Usage
    3  Offline Archives
      3.1  Usage
    4  Generation and Distribution
      4.1  Notes
    5  Support


Docker for Windows
##################

That would be the main reason to use Docker, as SCT can be installed
directly pretty much anywhere else.

Note: in case of problem, see `Support`_.

Docker runs natively only on Windows 10 Pro/Enterprise.
Download the docker installer from the `Docker official site
<https://store.docker.com/editions/community/docker-ce-desktop-windows/>`_

To Install Docker in Windows XP/VISTA/7/8/8.1/10 others than
Pro/Enterprise use `Docker Toolbox
<https://docs.docker.com/toolbox/overview/>`_.

Here is the the `tutorial
<https://docs.docker.com/toolbox/toolbox_install_windows/>`_.

When using Docker Toolbox, mounting folders in a docker container can
be a bit complicated and has certain limitations.
The main limitation is that by default we will only be able to mount
folders that are inside the ``C:/Users`` folder, for compatibility
reasons we will consider a shared folder under this folder, but it can
be changed.


To be able to process NIFTI volumes that we have in our Windows PC we
will go to the folder ``C:/Users`` and create a folder called
``docker_shared_folder`` This folder that we have just created will be
our work folder in which we will place all the volumes that we want to
process using the SCT.



Installation
************


#. Install `git <https://git-scm.com/download/win>`_ (in case you don't already have it), this is to provide
   an SSH binary.

#. Install `Xming <https://sourceforge.net/projects/xming/files/Xming/6.9.0.31/>`_.

#. Install `Docker <https://store.docker.com/editions/community/docker-ce-desktop-windows/>`_ (or `Docker Toolbox <https://docs.docker.com/toolbox/overview/>`_ depending of your Windows version).

#. Fetch the SCT image

   Either:

   - Online, from `Docker Hub <https://hub.docker.com/r/neuropoly/sct/>`_:

     Open CMD or if you are using Docker Toolbox open Docker Quickstart
     Terminal wait until get a prompt and run:

     .. code:: sh

        docker pull neuropoly/sct:sct-v4.0.0-beta.0-ubuntu-18.04

     Note: to list all available images on the registery, please see `Generation and distribution`_.

   - Local, from a downloaded archive

     Open CMD or if you are using Docker Toolbox open Docker Quickstart
     Terminal wait until get a prompt and run:

     .. code:: sh

        docker load --input sct-4.0.0-beta.0-ubuntu_18.04.tar

     **Note:** After the --input parameter you can include the complete
     path where the docker image is located.
     In the example it is assumed that the image is in the current
     directory.

#. If you are **NOT** using Docker Toolbox skip this step. To avoid
   memory issues when running the SCT is important to increment the
   default amount of RAM (1GB) of the Docker VM.
   To do this:

   Open Docker Quickstart Terminal wait until get a prompt and run:

   .. code:: sh

      docker-machine stop default

      /c/Program\ Files/Oracle/VirtualBox/VBoxManage.exe modifyvm default --memory 2048

      docker-machine start default

   **Note:** With these commands we have increased the RAM memory of
   the VM Docker to 2GB.
   It is important that your PC have at least 3 GB of RAM in order to
   leave at least 1 GB for your Windows host system.


#. For sharing folders between host and container:

   #. Go to `C:/Users` and create the folder named
      ``docker_shared_folder``

   #. If running Docker for Windows, click the Docker tray icon,
      run settings and allow sharing of your `C:` drive with the container,
      so as to allow access to the path.

#. Finally, reboot your computer after the installation.
   (Or you might end up with issues afterwards such as ``ssh: connect to host localhost port 2222: Cannot assign requested adress`` )

Usage
*****

#. Start throw-away container on the image.

   - If you are using Docker Toolbox, open Docker Quickstart Terminal
     wait until get a prompt and write:

     .. code:: sh

        docker run -p 2222:22 --rm -it -v //c/Users/docker_shared_folder://home/sct/docker_shared_folder neuropoly/sct:sct-v4.0.0-beta.0-ubuntu-18.04

   - If running Docker Desktop, run a different command:

     .. code:: sh

        docker run -p 2222:22 --rm -it -v c:/Users/docker_shared_folder://home/sct/docker_shared_folder neuropoly/sct:sct-v4.0.0-beta.0-ubuntu-18.04


   **Note:** The folder ``C:/Users/docker_shared_folder`` on the
   Windows host system will be linked to the folder
   ``/home/sct/docker_shared_folder`` inside the Docker container and
   the changes made to it will be visible for both the Docker
   container and the Windows system.

#.  Check the shared folder :

    - run command

    .. code:: sh

	ls

    - the docker_shared_folder should be highlighted in green : 
	.. image:: /picture/screenshot_green.PNG
	
      if not : 
	- check the permission on your local host file :
	    - go to C:/Users/
	    - right click on the folder open properties of the folder.
	    - go to the security tab 
		
	    - Check that the USER have full control over the folder.

	    .. image:: /picture/permission1.png

	    - if yes move on to next paragraph.

	    - if not change the permission and run the ls command again in the docker quickstart terminal. 
	    - if the folder is highlighted in green try creating a folder inside it.

	    .. code:: sh

		mkdir test

	    - Check if a new folder appeared in C:/Users/docker_folder_shared
	
		
	- Go to the docker quickstart terminal

		- Stop Docker Machine if it's running, by running command:

		.. code:: sh 

			docker-machine stop

		- Open VirtualBox GUI 
		
		- add a shared folder in the default machine setting :

			.. image:: ./picture/screenshot1.PNG

			click setting > shared folder and on the folder with a '+' sign

			.. image:: ./picture/screenshot2.PNG
 
			- Write C:\Users\docker_shared_folder in folder path

			- Write docker_shared_folder in Name textbox

			- Check Make Permanent and mount automatically boxes.

			.. image:: /picture/screenshot3.PNG 
 	
			- Go back to docker quickstart terminal.
 
		- Restart Docker Machine, by running command :

		.. code:: sh 

			docker-machine start

		- SSH into the Docker Machine, by running command 

		.. code:: sh

			docker-machine ssh

		- creat a new directory there by running :

		.. code:: sh 

			mkdir docker_shared_folder

		This will be /home/docker/docker_shared_folder.

		- Mount the Shared Folder you named above (docker_shared_folder) at the mount point you have created by running:

		.. code:: sh

 			sudo mount -t vboxsf -o uid=1000,gid=50 docker_shared_folder /home/docker/docker_shared_folder
		
		sudo password is sct unless you've changed it before
		
		- launch the container by running :
 
		.. code:: sh

			run docker run -p 2222:22 --rm -it -v /home/docker/docker_shared_folder://home/sct/docker_shared_folder neuropoly/sct:sct-v4.0.0-beta.0-ubuntu-18.04
		

		- check if the docker shared folder is highlighted in green after running:
		
		.. code:: sh 
			ls
 
		- if the folder is highlighted in green try creating a folder inside it.

	        .. code:: sh

		      mkdir test

	        - Check if a new folder appeared in C:/Users/docker_folder_shared

	

#. (NOT MANDATORY) Change the password (default is `sct`) from the
   container prompt:

   .. code:: sh

      passwd

#. Connect to it using Xming/SSH if X forwarding is needed
   (eg. running FSLeyes from there):

   Open a new CMD window and clone this repository:

   .. code:: sh

      git clone https://github.com/neuropoly/sct_docker.git

   If you are using Docker Desktop, run (double click) ``windows/sct-win.xlaunch``. If you are using Docker Toolbox,
   run ``windows/sct-win_docker_toolbox.xlaunch``

   If this is the first time you have done this procedure, the system
   will ask you if you want to add the remote PC (the docker
   container) as trust pc, type "yes" without "". Then type the
   password to enter the docker container (by default "sct" without
   "").

   The graphic terminal emulator LXterminal should appear, which
   allows copying and pasting commands, which makes it easier for
   users to use it.
   To check that X forwarding is working well write ``fsleyes &`` in
   LXterminal and FSLeyes should open, depending on how fast your
   computer is FSLeyes may take a few seconds to open.

   Notes:

   - If after closing a program with graphical interface (i.e. FSLeyes)
     LXterminal does not raise the shell ($) prompt then press Ctrl + C
     to finish closing the program.

   - Docker exposes the forwarded SSH server at different endpoints
     depending on whether Docker Desktop or Docker Toolbox is installed.

     Docker Desktop:

     .. code:: sh

        ssh -Y -p 2222 sct@127.0.0.1

     Docker Toolbox:

     .. code:: sh

        ssh -Y -p 2222 sct@192.168.99.100



Docker for UNIX (GNU/Linux, BSD family, MacOS)
##############################################


Installation
************

#. Install Docker

#. Fetch/install the SCT image:

   - If internet access, from `Docker Hub
     <https://hub.docker.com/r/neuropoly/sct/>`_:

     .. code:: sh

        docker pull neuropoly/sct:sct-v4.0.0-beta.0-ubuntu-18.04

   - Else, load the SCT image from a local file

     .. code:: sh

        docker load --input sct-v4.0.0-beta.0-ubuntu-18.04.tar

#. If you are on OSX and you need X forwarding (e.g. to run FSLeyes from the ssh window), install `Xquartz <https://www.xquartz.org/>`_.
   After installing Xquartz and after rebooting, run this command to prevent `this issue <https://github.com/neuropoly/sct_docker/issues/29>`_:

   .. code:: sh
   
      defaults write org.macosforge.xquartz.X11 enable_iglx -bool true


Usage
*****

#. Create a folder called ``docker_shared_folder`` in your home
   directory to be able to share information between your host system
   a the docker container.

   .. code:: sh

      mkdir ~/docker_shared_folder

#. Start throw-away container on the image:

   .. code:: sh

      docker run -p 2222:22 --rm -it -v ~/docker_shared_folder://home/sct/docker_shared_folder neuropoly/sct:sct-v4.0.0-beta.0-ubuntu-18.04


#. (NOT MANDATORY) Change the password (default is `sct`) from the container prompt:

   .. code:: sh

      passwd

#. Connect to container using SSH if X forwarding is needed
   (eg. running FSLeyes from there):

   .. code:: sh

      ssh -Y -p 2222 sct@localhost
   
#. Then enjoy SCT ;)


Offline Archives
################

Usage
*****

#. Extract archive in `/home/sct` (unfortunately due to hard-coded paths in the
   installation folder, this is mandatory):

   .. code:: sh

      cd $HOME
      tar xf /path/to/sct-v4.0.0-beta.0-ubuntu-18.04-offline.tar.xz

#. Add PATH:

   .. code:: sh

      PATH+=":/home/sct/sct_4.0.0-beta.0/bin"

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

For the official image that is released on docker hub we use the
Ubuntu 18.04 bas image.

List all available images in the registery (you will need `wget` for this to work):

.. code:: sh

  wget -q https://registry.hub.docker.com/v1/repositories/neuropoly/sct/tags -O -  | sed -e 's/[][]//g' -e 's/"//g' -e 's/ //g' | tr '}' '\n'  | awk -F: '{print $3}'

Example: creation of all distros container images:

.. code:: sh

   ./sct_docker_images.py generate --version v3.2.4

Example: creation of offline archive tarball:

.. code:: sh

   ./sct_docker_images.py generate --version v3.2.4 --distros ubuntu:18.04 --generate-distro-specific-sct-tarball

Example: creation and distribution:

.. code:: sh

   ./sct_docker_images.py generate --version v3.2.4 --publish-under neuropoly/sct


Notes
*****

- Caveat #1: When building images, specify a tag name or commit id, not a branch
  name, unless you have invalidated the Docker cache... or Docker will
  reuse whatever was existing and not test the right version

- Caveat #2: when building distro images, you may want to run `docker
  build` discarding the Docker cache, because commands such as
  `apt-get update` are cached leading to outdated package URLs.


Support
#######

Please try to differentiate issues about the SCT Docker packages or
tools, and SCT itself.

In case of problem, create issues `on the github project
<https://github.com/neuropoly/sct_docker/issues>`_ and provide information
allowing to quickly assist you.

Thank you!

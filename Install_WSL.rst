.. -*- coding: utf-8; indent-tabs-mode:nil; -*-

##########################
Spinal Cord Toolbox Docker
##########################

This documentation shows how to install the latest version of SCT. If you want install a different version of SCT please specify the version number you want.

.. contents::
..
    1  Windows subsystem for linux 
    2  environment preparation
    3  SCT installation 
    4  FSL installation 
    5  Usage 

Installation
************


#. Install `Xming <https://sourceforge.net/projects/xming/files/Xming/6.9.0.31/>`_.

#. Install `Windows subsystem for linux <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_ and initialize it.
	- Please install the Ubuntu 18.04 LTS distro. 

Environment preparation
***********************

Run the following command to install various packages that will be needed to install FSL and SCT. This will require your password

.. code-block:: sh

    sudo apt-get -y update
    sudo apt-get -y install gcc
    sudo apt-get -y install unzip
    sudo apt-get install -y python-pip python
    sudo apt-get install -y psmisc net-tools
    sudo apt-get install -y git
    sudo apt-get install -y gfortran
    sudo apt-get install -y libjpeg-dev
    echo 'export DISPLAY=127.0.0.1:0.0' >> .profile


Install SCT
*********** 

run the following command to download SCT:

.. code:: sh

    wget https://github.com/neuropoly/spinalcordtoolbox/archive/4.2.1.zip

Once the download is complete run this command to extract SCT from the zip archive:

.. code:: sh

    unzip 4.2.1.zip

Then go inside the folder by running:

.. code:: sh 

    cd spinalcordtoolbox-4.2.1

To install SCT run:

.. code:: sh
 
    yes | ./install_sct

To complete the installation you need to run:

.. code-block:: sh

    cd
    echo 'export SCT_DIR=/home/sct/sct_dev' >> .profile


Install FSL
***********

FSL contains fsleyes which is the default viewer for mifti image in SCT. 
Run this to download the installer and execute it:
 
.. code-block:: sh

    wget https://fsl.fmrib.ox.ac.uk/fsldownloads/fslinstaller.py
    python fslinstaller.py 

to complete the installation of these software run: 

.. code:: sh

    source .profile

You can now use SCT. To use FSLeyes, run Xming from your computer before entering the fsleyes command.

Your local C drive is located under '/mnt/c'. You can acces it by running `cd /mnt/c`


 

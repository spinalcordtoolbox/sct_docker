#!/usr/bin/env python3
# -*- coding: utf-8 vi:noet

import sys, io, os, logging, time, datetime, shutil


def generate(distro="debian:7", version="3.1.1"):
	"""
	"""

	frag = """
FROM {distro}
	""".strip().format(**locals())

	if distro.startswith(("debian", "ubuntu")):
		frag += "\n" + """
RUN apt-get update
RUN apt-get install -y curl sudo

# For conda
RUN apt-get install -y bzip2

# For remote GUI access
RUN apt-get install -y xorg
RUN apt-get install -y openssh-server
	""".strip()

	if distro.startswith(("fedora", "centos")):
		frag += "\n" + """
RUN dnf update -y
RUN dnf install -y curl sudo

# For conda
RUN dnf install -y bzip2

# For remote GUI access
RUN dnf install -y xorg-x11-twm xorg-x11-xauth
RUN dnf install -y openssh-server

# For SCT
RUN dnf install -y procps
	""".strip()


	frag += "\n" + """
RUN useradd -ms /bin/bash sct
RUN echo "sct ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN echo "sct:sct" | chpasswd
USER sct
ENV HOME /home/sct
WORKDIR /home/sct
EXPOSE 22
	""".strip()

	if version in ("3.1.1", "3.1.0"):
		frag += "\n" + """
RUN curl --location https://github.com/neuropoly/spinalcordtoolbox/archive/v{version}.tar.gz | gunzip | tar x && cd spinalcordtoolbox-{version} && yes | ./install_sct && cd - && rm -rf spinalcordtoolbox-{version}
#RUN echo export PATH+=":~/sct_{version}/bin" >> ~/.bashrc
#WORKDIR /home/sct/sct_{version}
#RUN echo $PATH TODO NG
		""".strip().format(**locals())
	else:
		frag += "\n" + """
RUN curl --location https://github.com/neuropoly/spinalcordtoolbox/archive/{version}.tar.gz | gunzip | tar x && cd spinalcordtoolbox-{version} && yes | ./install_sct && cd - && rm -rf spinalcordtoolbox-{version}
RUN echo export PATH+=":~/sct_dev/bin" >>~/.bashrc
#RUN . ~/.bashrc; sct_download_data -d sct_example_data
		""".strip().format(**locals())

	frag += "\n" + """

# Get sct_example_data for offline use
RUN sct_download_data -d sct_example_data

# QC connection
EXPOSE 8888

RUN yes '' | sudo ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key

RUN echo  X11UseLocalhost no | sudo tee --append /etc/ssh/sshd_config

ENTRYPOINT bash -c 'sudo /usr/sbin/sshd; /bin/bash'
	""".strip()

	name = "sct-%s-%s" % (distro.replace(":", "-"), version)
	if not os.path.exists(name):
		os.makedirs(name)
	with io.open(os.path.join(name, "Dockerfile"), "w") as f:
		f.write(frag)

	logging.info("You can now run: docker build -t %s %s", name, name)

	return name


if __name__ == "__main__":

	import argparse


	logger = logging.getLogger()
	#logger.addHandler(logging.StreamHandler(sys.stdout))
	logger.setLevel(logging.DEBUG)#INFO)


	parser = argparse.ArgumentParser(
	 description="SCT + Docker",
	)

	subparsers = parser.add_subparsers(
	 help='the command; type "%s COMMAND -h" for command-specific help' % sys.argv[0],
	 dest='command',
	)

	subp = subparsers.add_parser(
	 "generate",
	 help="Generate a Docker file",
	)

	subp.add_argument("--distro",
	 default="ubuntu:16.04",
	 help="Distribution to use (docker image)",
	)

	subp.add_argument("--version",
	 default="3.1.1",
	)

	try:
		import argcomplete
		argcomplete.autocomplete(parser)
	except:
		pass

	args = parser.parse_args()

	if args.command == "generate":
		res = generate(distro=args.distro, version=args.version)
		print(res)


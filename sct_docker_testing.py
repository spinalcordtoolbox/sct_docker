#!/usr/bin/env python3
# -*- coding: utf-8 vi:noet
# Testing using Docker

import sys, io, os, logging, time, datetime, shutil, datetime, subprocess

import sct_docker

default_distros = (
 "ubuntu:16.04",
)

default_version = "master"

default_commands = [
 "sct_testing -d 0",
 "${SCT_DIR}/batch_processing.sh -nodownload",
]

def run_test(distros=None, version=None, commands=None):
	"""
	"""

	if distros is None:
		distros = default_distros

	if version is None:
		version = default_version

	if commands is None:
		commands = default_commands

	names = []
	for distro in distros:
		name = "sct-testing-{}-{}-{}".format(distro.replace(":", "-"), version, datetime.datetime.now().strftime("%Y%m%d%H%M%S")).lower()

		name = sct_docker.generate(distro=distro, version=version, commands=commands, name=name)

		names.append(name)

	for name in names:
		cmd = [
		 "docker", "build", "-t", name, name,
		]
		print(cmd)
		subprocess.call(cmd)


if __name__ == "__main__":

	import argparse


	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)


	parser = argparse.ArgumentParser(
	 description="SCT + Docker + Testing",
	)

	subparsers = parser.add_subparsers(
	 help='the command; type "%s COMMAND -h" for command-specific help' % sys.argv[0],
	 dest='command',
	)

	subp = subparsers.add_parser(
	 "test",
	 help="Test a distro/version/command",
	)

	subp.add_argument("--distros",
	 nargs="+",
	 help="Distributions to test (docker image names)",
	 default=default_distros,
	)

	subp.add_argument("--version",
	 default=default_version,
	)

	subp.add_argument("--commands",
	 nargs="+",
	 default=default_commands,
	)

	try:
		import argcomplete
		argcomplete.autocomplete(parser)
	except:
		pass

	args = parser.parse_args()

	if args.command == "test":
		res = run_test(distros=args.distros, version=args.version)


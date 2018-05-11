#!/usr/bin/env python3
# -*- coding: utf-8 vi:noet
# Testing using Docker

import sys, io, os, logging, time, datetime, shutil, datetime, subprocess

import sct_docker


if sys.hexversion < 0x03030000:
    import pipes
    def list2cmdline(lst):
        return " ".join(pipes.quote(x) for x in lst)
else:
    import shlex
    def list2cmdline(lst):
        return " ".join(shlex.quote(x) for x in lst)


default_distros = (
 "ubuntu:14.04",
 "ubuntu:16.04",
 "ubuntu:18.04",
 "debian:7",
 "debian:8",
 "debian:9",
 "fedora:25",
 "fedora:26",
 "fedora:27",
 #"centos:6", #https://github.com/neuropoly/spinalcordtoolbox/issues/1704
 "centos:7",
)

default_version = "master"

default_commands = [
 "MPLBACKEND=Agg sct_testing -d 0",
 "MPLBACKEND=Agg ${SCT_DIR}/batch_processing.sh -nodownload",
]

def run_test(distros=None, version=None, commands=None, jobs=None):
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

		name = sct_docker.generate(distro=distro, version=version, commands=commands,
		 name=name, configure_ssh=False)

		names.append(name)


	from multiprocessing.pool import ThreadPool
	pool = ThreadPool(jobs)

	res = list()
	for name in names:

		cmd = [
		 "docker", "build", "-t", name, name,
		]

		promise = pool.apply_async(lambda x: subprocess.call(x), (cmd,))
		res.append(promise)

	errs = list()
	for name, promise in zip(names, res):
		err = promise.get()
		if err != 0:
			logging.error("{} failed with error code {}".format(name, err))
		errs.append(err)

	pool.close()
	x = pool.join()

	for name, err in zip(names, errs):
		if err == 0:
			logging.info("{} finished successfully".format(name))
		else:
			logging.error("{} failed with error code {}".format(name, err))
	print(errs)

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

	subp.add_argument("--jobs",
	 type=int,
	 default=None,
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
		res = run_test(distros=args.distros, version=args.version,
		 commands=args.commands, jobs=args.jobs)


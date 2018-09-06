#!/usr/bin/env python3
# -*- coding: utf-8 vi:noet
# Testing using Docker

import sys, io, os, logging, time, datetime, shutil, datetime, subprocess

import sct_docker
from sct_docker import printf, check_exe

default_distros = (
 "ubuntu:14.04",
 "ubuntu:16.04",
 "ubuntu:18.04",
 #"debian:7", # has issues with installing wxPython (fsleyes dep)
 "debian:8",
 "debian:9",
 "fedora:25",
 "fedora:26",
 "fedora:27",
 "fedora:28",
 "centos:7",
)

official_distro = "ubuntu:18.04"

default_version = "master"

default_commands = (
)

def generate(distros=None, version=None,
 jobs=None,
 publish_under=None,
 generate_docker_tarball=False,
 generate_distro_specific_sct_tarball=False,
 ):
	"""
	"""

	if distros is None:
		distros = default_distros

	if version is None:
		version = default_version

	print("Generating distro Dockerfiles")
	names = []
	for distro in distros:
		name = "sct-{}-{}".format(version, distro.replace(":", "-")).lower()
		printf("- %s..." % name)

		name = sct_docker.generate(distro=distro, version=version,
		 name=name, commands=default_commands,
		 install_fsleyes=True,
		 install_tools=True,
		 #install_fsl=True,
		 configure_ssh=True,
		 verbose=False,
		)

		names.append(name)

		if distro == official_distro:
			name = "sct-{}-{}".format(version, "official").lower()
			printf("- %s..." % name)

			name = sct_docker.generate(distro=distro, version=version,
			 name=name, commands=default_commands,
			 install_fsleyes=True,
			 #install_fsl=True,
			 configure_ssh=True,
			 verbose=False,
			)

			names.append(name)

		print("")
	print("Done generating distro Dockerfiles")

	print("Building images")

	if not check_exe("docker"):
		raise RuntimeError("You might want to have docker available when running this tool")

	from multiprocessing.pool import ThreadPool
	pool = ThreadPool(jobs)

	try:
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
	except BaseException as e:
		print("Keyboard interrupt")
		pool.terminate()
		raise SystemExit(1)
	pool.join()
	print("Done building images")

	failed = False
	for name, err in zip(names, errs):
		if err == 0:
			logging.info("{} finished successfully".format(name))
		else:
			logging.error("{} failed with error code {}".format(name, err))
			failed = True

	if failed:
		print(errs)
		logging.error("Not proceeding further as one distro failed")
		return 1

	if publish_under:
		print("Publishing on Docker hub")
		for name in names:
			printf("- %s..." % name)
			cmd = ["docker", "tag", name, "{}:{}".format(publish_under, name)]
			subprocess.call(cmd)
			cmd = ["docker", "push", "{}:{}".format(publish_under, name)]
			subprocess.call(cmd)
			print("")
		print("Done publishing")

	if generate_docker_tarball:
		print("Generating Docker tarballs")
		for name in names:
			printf("- %s..." % name)
			cmd = ["bash", "-c", "docker save {}" \
			 " | xz --threads=0 --best > {}-docker.tar.xz".format(name, name)]
			subprocess.call(cmd)
			print("")
		print("Done generating Docker tarballs")

	if generate_distro_specific_sct_tarball:

		print("Generating offline archives")
		if not (check_exe("xz") and check_exe("bash")):
			raise RuntimeError("You might want to have bash & xz available when running this tool")
		for name in names:
			printf("- %s..." % name)
			cmd = ["bash", "-c", "docker run --log-driver=none --entrypoint /bin/sh {} -c 'cd /home/sct; tar c sct_*'" \
			 " | xz --threads=0 --best > {}-offline.tar.xz".format(name, name)]
			subprocess.call(cmd)
			print("")
		print("Done generating offline archives")


if __name__ == "__main__":

	import argparse


	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)


	parser = argparse.ArgumentParser(
	 description="SCT + Docker Official Image Generation",
	)

	subparsers = parser.add_subparsers(
	 help='the command; type "%s COMMAND -h" for command-specific help' % sys.argv[0],
	 dest='command',
	)

	subp = subparsers.add_parser(
	 "generate",
	 help="Build a distro/version",
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

	subp.add_argument("--generate-docker-tarball",
	 action="store_true",
	 default=False,
	)

	subp.add_argument("--generate-distro-specific-sct-tarball",
	 action="store_true",
	 default=False,
	)

	subp.add_argument("--publish-under",
	 help="Where to publish on docker hub (x/y)",
	)

	try:
		import argcomplete
		argcomplete.autocomplete(parser)
	except:
		pass

	args = parser.parse_args()

	if args.command == "generate":
		res = generate(distros=args.distros, version=args.version,
		 generate_docker_tarball=args.generate_docker_tarball,
		 generate_distro_specific_sct_tarball=args.generate_distro_specific_sct_tarball,
		 publish_under=args.publish_under,
		 jobs=args.jobs)
		raise SystemExit(res)
	else:
		parser.print_help(sys.stderr)
		raise SystemExit(1)

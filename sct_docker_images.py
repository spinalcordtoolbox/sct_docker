#!/usr/bin/env python3
# -*- coding: utf-8 vi:noet
# Testing using Docker

import sys, io, os, logging, time, datetime, shutil, datetime, subprocess
import threading
import multiprocessing.pool

import sct_docker
from sct_docker import printf, check_exe

logger = logging.getLogger(__name__)


default_distros = (
 "official",
 #"ubuntu:14.04",
 "ubuntu:16.04",
 "ubuntu:18.04",
 "ubuntu:19.04",
 #"debian:7", # has issues with installing wxPython (fsleyes dep)
 "debian:8",
 "debian:9",
 "fedora:25",
 "fedora:26",
 "fedora:27",
 "fedora:28",
 "fedora:29",
 "fedora:30",
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
 build_options=[],
 proxy=False,
 ):
	"""
	"""

	if distros is None:
		distros = default_distros

	if version is None:
		version = default_version

	logger.info("Generating distro Dockerfiles")
	names = []
	for distro in distros:
		name = "sct-{}-{}".format(version, distro.replace(":", "-")).lower()
		logger.info("- %s...", name)

		lock = threading.Lock() # prevent building official simultaneously to alias

		name = sct_docker.generate(distro=distro, version=version,
		 name=name, commands=default_commands,
		 install_fsleyes=True,
		 install_tools=True,
		 #install_fsl=True,
		 configure_ssh=True,
		 verbose=False,
		 proxy=proxy,
		)

		names.append((name, lock))

		if distro == "official":
			name = "sct-{}-{}".format(version, "official").lower()
			logger.info("- %s...", name)

			name = sct_docker.generate(distro=official_distro, version=version,
			 name=name, commands=default_commands,
			 install_fsleyes=True,
			 #install_fsl=True,
			 configure_ssh=True,
			 verbose=False,
			 proxy=proxy,
			)

			names.append((name, lock))

	logger.info("Done generating distro Dockerfiles")

	logger.info("Building images")

	if not check_exe("docker"):
		raise RuntimeError("You might want to have docker available when running this tool")

	pool = multiprocessing.pool.ThreadPool(jobs)

	try:
		res = list()
		for name, lock in names:

			cmd = [
			 "docker", "build",
			 "-t", name, name,
			] + build_options

			def docker_build(cmd, lock):
				with lock:
					return subprocess.call(cmd)

			promise = pool.apply_async(docker_build, (cmd, lock))
			res.append(promise)

		errs = list()
		for (name, _), promise in zip(names, res):
			err = promise.get()
			if err != 0:
				logging.error("{} failed with error code {}".format(name, err))
			errs.append(err)

		pool.close()
	finally:
		pool.terminate()
	pool.join()
	logger.info("Done building images")

	failed = False
	for (name,_), err in zip(names, errs):
		if err == 0:
			logging.info("{} finished successfully".format(name))
		else:
			logging.error("{} failed with error code {}".format(name, err))
			failed = True

	if failed:
		logging.error("Not proceeding further as one distro failed: %s", errs)
		raise RuntimeError("Failed generating one distro")

	if proxy:
		return

	if publish_under:
		logger.info("Publishing on Docker hub")
		for name,_ in names:
			logger.info("- %s...", name)
			cmd = ["docker", "tag", name, "{}:{}".format(publish_under, name)]
			subprocess.call(cmd)
			cmd = ["docker", "push", "{}:{}".format(publish_under, name)]
			subprocess.call(cmd)

		logger.info("Done publishing")

	if generate_docker_tarball:
		logger.info("Generating Docker tarballs")
		for name,_ in names:
			logger.info("- %s...", name)
			cmd = ["bash", "-c", "docker save {}" \
			 " | xz --threads=0 --best > {}-docker.tar.xz".format(name, name)]
			subprocess.call(cmd)
		logger.info("Done generating Docker tarballs")

	if generate_distro_specific_sct_tarball:

		logger.info("Generating offline archives")
		if not (check_exe("xz") and check_exe("bash")):
			raise RuntimeError("You might want to have bash & xz available when running this tool")
		for name,_ in names:
			logger.info("- %s...", name)
			cmd = ["bash", "-c", "docker run --log-driver=none --entrypoint /bin/sh {} -c 'cd /home/sct; tar c sct_*'" \
			 " | xz --threads=0 --best > {}-offline.tar.xz".format(name, name)]
			subprocess.call(cmd)

		logger.info("Done generating offline archives")


def main():
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
	 default=["official"],
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


	subp.add_argument("--proxy",
	 action="store_true",
	 default=False,
	)

	try:
		import argcomplete
		argcomplete.autocomplete(parser)
	except:
		pass

	args = parser.parse_args()

	if args.command == "generate":
		return generate(distros=args.distros, version=args.version,
		 generate_docker_tarball=args.generate_docker_tarball,
		 generate_distro_specific_sct_tarball=args.generate_distro_specific_sct_tarball,
		 publish_under=args.publish_under,
		 jobs=args.jobs,
		 proxy=args.proxy,
		)
	else:
		parser.print_help(sys.stderr)
		return 1

if __name__ == "__main__":
	res = main()
	raise SystemExit(res)

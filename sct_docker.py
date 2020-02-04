#!/usr/bin/env python3
# -*- coding: utf-8 vi:noet

import sys, io, os, re, logging, time, datetime, shutil

logger = logging.getLogger(__name__)

if sys.hexversion < 0x03030000:
    import pipes


    def list2cmdline(lst):
        return " ".join(pipes.quote(x) for x in lst)
else:
    import shlex


    def list2cmdline(lst):
        return " ".join(shlex.quote(x) for x in lst)


def printf(x):
    sys.stdout.write(x)
    sys.stdout.flush()


def check_exe(name):
    """
    Ensure that a program exists
    :type name: string
    :param name: name or path to program
    :return: path of the program or None
    """

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(name)
    if fpath and is_exe(name):
        return fpath
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, name)
            if is_exe(exe_file):
                return exe_file


def generate(distro="debian:7", version="3.1.1", commands=None, name=None,
             install_python=True,
             install_compilers=False,
             install_tools=False,
             install_fsleyes=False,
             install_fsl=False,
             configure_ssh=True,
             verbose=True,
             proxy=False,
             ):
    """
    :param distro: Distribution (Docker specification)
    :param version: SCT version
    :param commands: Commands to run as part of build
    :returns: name
    """

    frag = """
    FROM {distro}
    """.strip().format(**locals())

    # This docker variable will be needed to strip the unwanted spaces at the end. We just initialize it here. 
    docker = ''

    if "/" in distro:
        orga, distro = distro.split("/")
        distro = "%s@%s" % (distro, orga)

    if distro.startswith(("debian", "ubuntu")):
        frag += "\n" + """
        RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
        RUN apt-get update --fix-missing
        RUN apt-get install -y curl vim 

        # For Qc message
        ENV DOCKER=yes
        """.strip()

    elif distro in ("centos:6", "centos:7",):
        frag += "\n" + """
        RUN yum update -y
        RUN yum install -y curl
        """.strip()

    elif distro.startswith(("fedora", "centos")):
        frag += "\n" + """
        RUN dnf update -y
        RUN dnf install -y curl
        """.strip()

    if proxy:
        if distro.startswith(("debian", "ubuntu")):
            frag += "\n" + """
            RUN apt-get install -y ca-certificates
            ENV CERTDIR=/etc/ssl/certs
            ENV CERTECHO=echo
            """.strip()

        elif distro in ("centos:6", "centos:7",):
            frag += "\n" + """
            RUN yum install -y ca-certificates
            ENV CERTDIR=/etc/pki/ca-trust/source/anchors
            ENV CERTECHO="echo -e"
            """.strip()

        elif distro.startswith(("fedora", "centos")):
            frag += "\n" + """
            RUN dnf install -y ca-certificates
            ENV CERTDIR=/etc/pki/ca-trust/source/anchors
            ENV CERTECHO="echo -e"
            """.strip()

        # Use CA certificate for local ssl_bump proxy
        frag += "\n" + """
        RUN ${CERTECHO} "-----BEGIN CERTIFICATE-----\\nMIIDyTCCArGgAwIBAgIJAKF6rNGHC1AeMA0GCSqGSIb3DQEBCwUAMHsxCzAJBgNV\\nBAYTAkNBMQ8wDQYDVQQIDAZRdWViZWMxETAPBgNVBAcMCE1vbnRyZWFsMQ0wCwYD\\nVQQKDARub25lMRQwEgYDVQQDDAt6b3VnbG91Yi5ldTEjMCEGCSqGSIb3DQEJARYU\\nY0otc3F1aWRAem91Z2xvdWIuZXUwHhcNMTkwNzI3MjMwMzA1WhcNMjAwNzI2MjMw\\nMzA1WjB7MQswCQYDVQQGEwJDQTEPMA0GA1UECAwGUXVlYmVjMREwDwYDVQQHDAhN\\nb250cmVhbDENMAsGA1UECgwEbm9uZTEUMBIGA1UEAwwLem91Z2xvdWIuZXUxIzAh\\nBgkqhkiG9w0BCQEWFGNKLXNxdWlkQHpvdWdsb3ViLmV1MIIBIjANBgkqhkiG9w0B\\nAQEFAAOCAQ8AMIIBCgKCAQEAwyt/Iv5PE6hbWngoIDAY3zKh1V9luuyfweSs4/tg\\nz5btY1j+PqMOl2MpcYsVW7+HwqJq5E6jn2qMPA94XwfnylQqUL/rpC+90Lt964k0\\nVhQi5FhQkyW3R5WaN03cn2xyj4wsiSyPDP61274DpkymhXflCYsKp0Ta3C8VUV8U\\nPqEpzWwPdfi4Ej5XFidXGKdeE6JZftypFK2wyIA+cwbZE/MP7pp6BvoyIJsV5duq\\njF9ByhAtdka8B8IzBVtp87HjeT7MHAjHtrzddaW/s8Dfnr4HkQb+t2ZBDxlUDvWY\\n0jERTcToobfXU3TjRMPriQnbb4cDfbbbqUKucUw2c8aXaQIDAQABo1AwTjAdBgNV\\nHQ4EFgQU9PnADlRycQCVXhOaGre9oF6WrHswHwYDVR0jBBgwFoAU9PnADlRycQCV\\nXhOaGre9oF6WrHswDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAFPlT\\nZBs2zOI7CiNixIO7G3QFQKRUheFAQMll0w9FXQW+3aB7TcKtsu6iR0oIPoXx50G8\\nX1uaxi9CidO98yI1QLvnxZlumvX9peRooFryyUGrzN8Fiy8hdTtuS9KNzWDgVApj\\nIcqYr53RM/jzIS4AHRwaau8wrWaoiys3wvHKhNL9EH5I7WzKHS0elrjW5Mn4Ew0i\\n3gQ+rQ5VoL0Ljm8GA2EJQ9gzecdvShMuXAMFokte0BRvYwHEM4+mkGVoTdPrN/pf\\n2xnk91vA0AQnYbrottxGIpL9WwRSjyz8qQv/Nw8S2ohauJz3aDXcUNXOCm6RZ7Vl\\noSqg2oypaL1o9/b20g==\\n-----END CERTIFICATE-----" > ${CERTDIR}/zougloub.eu.pem
        RUN cat ${CERTDIR}/zougloub.eu.pem
        ENV https_proxy=http://zougloub.eu:3128 http_proxy=http://zougloub.eu:3128
        """.strip()

        if distro.startswith(("debian", "ubuntu")):
            frag += "\n" + """
            RUN update-ca-certificates --verbose --fresh
            """.strip()

        elif distro.startswith(("centos", "fedora")):
            frag += "\n" + """
            RUN update-ca-trust
            """.strip()

        if distro == "centos:6":
            # https://www.happyassassin.net/2015/01/14/trusting-additional-cas-in-fedora-rhel-centos-dont-append-to-etcpkitlscertsca-bundle-crt-or-etcpkitlscert-pem/
            frag += "\n" + """
            RUN update-ca-trust enable
            """.strip()

    if distro.startswith(("debian", "ubuntu")):
        frag += "\n" + """
        RUN apt-get install -y sudo
        # For conda
        RUN apt-get install -y bzip2

        # For remote GUI access
        RUN apt-get install -y xorg xterm lxterminal
        RUN apt-get install -y openssh-server
        """.strip()

    elif distro in ("centos:6", "centos:7",):
        frag += "\n" + """
        RUN yum install -y sudo

        # For conda
        RUN yum install -y bzip2

        # For remote GUI access
        RUN yum install -y xorg-x11-twm xorg-x11-xauth xterm lxterminal
        RUN yum install -y openssh-server

        # For SCT
        RUN yum install -y procps findutils which
        RUN yum search libstdc
        RUN yum install -y compat-libstdc++-33 libstdc++
        """.strip()

    elif distro.startswith(("fedora", "centos")):
        frag += "\n" + """
        RUN dnf install -y sudo

        # For conda
        RUN dnf install -y bzip2

        # For remote GUI access
        RUN dnf install -y xorg-x11-twm xorg-x11-xauth xterm lxterminal
        RUN dnf install -y openssh-server

        # For SCT
        RUN dnf install -y procps findutils which
        RUN dnf search libstdc
        RUN dnf install -y compat-libstdc++-33 libstdc++
        """.strip()

    if install_fsleyes or install_fsl or install_compilers:
        if distro.startswith(("debian", "ubuntu")):
            frag += "\n" + """
            RUN apt-get update --fix-missing
            RUN apt-get install -y build-essential
            """.strip()

        elif distro.startswith("fedora"):
            frag += "\n" + """
            # dnf groupinstall -y "Development Tools"
            RUN dnf install -y redhat-rpm-config gcc "gcc-c++" make
            """.strip()

        elif distro.startswith("centos"):
            frag += "\n" + """
            RUN yum install -y redhat-rpm-config gcc "gcc-c++" make
            """.strip()

    if install_fsleyes:
        if distro.startswith(("debian", "ubuntu")):
            frag += "\n" + """
            RUN apt-get install -y python-pip
            """.strip()

        elif distro.startswith("fedora"):
            frag += "\n" + """
            RUN dnf install -y python-pip python-devel
            """.strip()

        elif distro.startswith("centos"):
            frag += "\n" + """
            #RUN yum install -y epel-release
            RUN yum install -y python-pip python-devel
            """.strip()

        if distro in ("debian:7",):
            frag += "\n" + """
            RUN apt-get install -y libgtkmm-3.0-dev libgtkglext1-dev libgtk-3-dev
            RUN apt-get install -y libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev
            RUN apt-get install -y libwebkitgtk-3.0-dev libwebkitgtk-dev
            """.strip()

        elif distro == "ubuntu:19.04":
            frag += "\n" + """
            RUN apt-get install -y libgtkmm-3.0-dev libgtkglext1-dev
            RUN apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
            #RUN apt-get install -y libwebkitgtk-3.0-dev libwebkitgtk-dev
            """.strip()

        elif distro.startswith(("debian", "ubuntu")):
            frag += "\n" + """
            RUN apt-get install -y freeglut3-dev
            RUN apt-get install -y libgtkmm-3.0-dev libgtkglext1-dev
            RUN apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
            RUN apt-get install -y libwebkitgtk-3.0-dev libwebkitgtk-dev
            """.strip()

        elif distro in ("fedora:27", "fedora:28", "fedora:29", "fedora:30"):
            frag += "\n" + """
            RUN dnf install -y gtkmm30-devel gtkglext-devel
            RUN dnf install -y gstreamer1-devel gstreamer1-plugins-base-devel
            RUN dnf install -y webkitgtk4-devel
            """.strip()

        elif distro in ("fedora:25", "fedora:26",):
            frag += "\n" + """
            RUN dnf install -y gtkmm30-devel gtkglext-devel freeglut-devel
            RUN dnf install -y gstreamer1-devel gstreamer1-plugins-base-devel
            RUN dnf install -y webkitgtk3-devel webkitgtk-devel
            """.strip()

        elif distro.startswith("centos"):
            frag += "\n" + """
            RUN yum install -y gtkmm30-devel gtkglext-devel freeglut-devel
            RUN yum install -y gstreamer1-devel gstreamer1-plugins-base-devel
            RUN yum install -y webkitgtk3-devel webkitgtk-devel
            """.strip()

    if install_fsl:
        if distro.startswith("fedora"):
            frag += "\n" + """
            RUN dnf install -y expat-devel libX11-devel mesa-libGL-devel zlib-devel
            """.strip()

        elif distro.startswith("centos"):
            frag += "\n" + """
            RUN yum install -y expat-devel libX11-devel mesa-libGL-devel zlib-devel
            """.strip()

        elif distro.startswith(("ubuntu", "debian")):
            frag += "\n" + """
            RUN apt-get install -y libexpat1-dev libx11-dev zlib1g-dev libgl1-mesa-dev
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

    if proxy:
        frag += "\n" + """
    ENV https_proxy=http://zougloub.eu:3128 http_proxy=http://zougloub.eu:3128 HTTPS_PROXY=http://zougloub.eu:3128 HTTP_PROXY=http://zougloub.eu:3128
    ENV REQUESTS_CA_BUNDLE=${CERTDIR}/zougloub.eu.pem
    """.strip()

    if install_tools:

        if distro.startswith("fedora"):
            frag += "\n" + """
            RUN sudo dnf install -y psmisc net-tools
            """.strip()

        elif distro.startswith("centos"):
            frag += "\n" + """
            RUN sudo yum install -y psmisc net-tools
            """.strip()

        elif distro.startswith(("ubuntu", "debian")):
            frag += "\n" + """
            RUN sudo apt-get install -y psmisc net-tools
            """.strip()

    if distro.startswith("fedora"):
        frag += "\n" + """
        RUN sudo dnf install -y git
        """.strip()

    elif distro.startswith("centos"):
        frag += "\n" + """
        RUN sudo yum install -y git
        """.strip()

    elif distro.startswith(("ubuntu", "debian")):
        frag += "\n" + """
        RUN sudo apt-get install -y git
        """.strip()

    if proxy:

        if distro in ("debian:8",):
            frag += "\n" + """
            RUN git config --global http.sslCAInfo /etc/ssl/certs/zougloub.eu.pem
            """.strip()

    if install_python:

        if distro in ("debian:8", "ubuntu:14.04"):
            frag += "\n" + """
            # Install more fsleyes dependencies
            RUN sudo apt-get install -y python3 python3-dev
            RUN sudo apt-get install -y python3-pip
            RUN sudo apt-get install -y liblapack-dev
            RUN sudo apt-get install -y gfortran

            # for pillow
            RUN sudo apt-get install -y libjpeg-dev


            ENV PYTHON python3

            RUN mkdir -p ~/.local/bin
            RUN ln -sf $(which ${PYTHON}) ~/.local/bin/python
            """.strip()

        elif distro in ("debian:7", "debian:8", "debian:9") or distro.startswith("ubuntu"):
            frag += "\n" + """
            # Install more fsleyes dependencies
            RUN sudo apt-get install -y python3-dev
            RUN sudo apt-get install -y python3-pip
            RUN sudo apt-get install -y liblapack-dev
            RUN sudo apt-get install -y gfortran

            # for pillow
            RUN sudo apt-get install -y libjpeg-dev

            ENV PYTHON python3

            RUN mkdir -p ~/.local/bin
            RUN ln -sf $(which ${PYTHON}) ~/.local/bin/python
            """.strip()

        elif distro.startswith("fedora"):
            frag += "\n" + """
            # Install more fsleyes dependencies
            RUN sudo dnf install -y python3 python3-devel
            ENV PYTHON python3
            RUN ${PYTHON} --version
            RUN which ${PYTHON}
            RUN echo ${PATH}
            """.strip()

        if distro in ("centos:7",):
            # https://linuxize.com/post/how-to-install-python-3-on-centos-7/
            frag += "\n" + """
            # Install more fsleyes dependencies
            RUN sudo yum install -y centos-release-scl
            RUN sudo yum install -y rh-python36
            RUN scl enable rh-python36 bash; which python
            RUN mkdir -p ~/.local/bin
            RUN ln -sf /opt/rh/rh-python36/root/usr/bin/python ~/.local/bin/python3
            ENV PYTHON /opt/rh/rh-python36/root/usr/bin/python
            """.strip()

        frag += "\n" + """
        SHELL ["/bin/bash", "-c"]
        RUN echo 'PATH=\"${PATH}:${HOME}/.local/bin\"' >> ~/.bashenv
        ENV BASH_ENV ~/.bashenv
        """.strip()

    m = re.match(r"^(?P<v>v)?(?P<pv>\d+\.\d+\.\d+(-beta\.\d+)?)$", version)
    if m is not None:
        dirv = m.group("pv")
        dl_fn = version  # if version.startswith("v") else "v{}".format(version)
        sct_dir = "/home/sct/sct_{}".format(dirv)
        frag += "\n" + """
        RUN curl --location https://github.com/neuropoly/spinalcordtoolbox/archive/{dl_fn}.tar.gz | gunzip | tar x && cd spinalcordtoolbox-{dirv} && yes | ./install_sct && cd - && rm -rf spinalcordtoolbox-{dirv}
        """.strip().format(**locals())
    else:
        dirv = version
        sct_dir = "/home/sct/sct_dev"
        frag += "\n" + """
        RUN curl --location https://github.com/neuropoly/spinalcordtoolbox/archive/{version}.tar.gz | gunzip | tar x && cd spinalcordtoolbox-{dirv}* && yes | ./install_sct && cd - && rm -rf spinalcordtoolbox-{dirv}*
        """.strip().format(**locals())

    frag += "\n" + """
    ENV SCT_DIR {sct_dir}
    """.strip().format(**locals())

    frag += "\n" + """
    # Get data for offline use
    RUN bash -i -c "sct_download_data -d sct_example_data"
    RUN bash -i -c "sct_download_data -d sct_testing_data"
    """.strip()

    if install_fsleyes:

        if distro in ("debian:8", "ubuntu:14.04"):
            frag += "\n" + """
        # for matplotlib wxagg support
        """.strip()

        elif distro in ("debian:7", "debian:8", "debian:9") or distro.startswith("ubuntu"):
            frag += "\n" + """
            """.strip()

        elif distro.startswith("fedora"):
            frag += "\n" + """
            """.strip()

        if distro in ("centos:7",):
            # https://linuxize.com/post/how-to-install-python-3-on-centos-7/
            frag += "\n" + """
            """.strip()

        if proxy and False:
            # unneeded due to REQUESTS_CA_BUNDLE
            frag += "\n" + """
            ENV PIP ${PYTHON} -m pip --cert ${CERTDIR}/zougloub.eu.pem
            """.strip()
        else:
            frag += "\n" + """
            ENV PIP ${PYTHON} -m pip
            """.strip()

        if distro in ("centos:7",):
            # https://linuxize.com/post/how-to-install-python-3-on-centos-7/
            frag += "\n" + """
            RUN bash -i -c "echo 'PATH=\"${HOME}/.local/bin:${PATH}\"' >> ~/.bashrc"
            """.strip()  # TODO

        frag += "\n" + """
        # can't use system packages as they'd get updated
        RUN ${PIP} install --user --upgrade pathlib2
        RUN ${PIP} install --user --upgrade pip
        RUN ${PIP} install --user --upgrade setuptools
        RUN ${PIP} install --user --upgrade numpy
        RUN ${PIP} install --user --upgrade scipy
        RUN ${PIP} install --user --upgrade Pillow
        RUN ${PIP} install --user --upgrade wxPython
        # :| wxPython/ext/wxWidgets/src/gtk/settings.cpp:260:29: error: 'GTK_TYPE_HEADER_BAR' was not declared in this scope
        RUN ${PIP} install --user --upgrade cython
        """.strip()

        frag += "\n" + """
        # Workaround https://github.com/mcfletch/pyopengl/issues/11
        RUN git clone https://github.com/mcfletch/pyopengl && cd pyopengl && ${PIP} install --user --upgrade . && cd accelerate && ${PIP} install --user --upgrade .
        """.strip()

        frag += "\n" + """
        RUN ${PIP} install --user fsleyes
        """.strip()

    if install_fsl:
        # TODO WIP
        # https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation/SourceCode
        # https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation/ShellSetup

        frag += "\n" + """
        RUN bash -c "curl https://fsl.fmrib.ox.ac.uk/fsldownloads/fsl-5.0.11-sources.tar.gz | gunzip | tar x"
        """.strip()

        frag += "\n" + """
        ENV FSLDIR /home/sct/fsl
        RUN bash -c ". ${FSLDIR}/etc/fslconf/fsl.sh; ls ${FSLDIR}/config/\${FSLMACHTYPE}"
        RUN bash -c ". ${FSLDIR}/etc/fslconf/fsl.sh; cd ${FSLDIR}; ./build"
        RUN bash -c ". ${FSLDIR}/etc/fslconf/fsl.sh; ${FSLDIR}/etc/fslconf/post_install.sh -f ${FSLDIR}"
        RUN bash -c ". ${FSLDIR}/etc/fslconf/fsl.sh; ${FSLDIR}/etc/fslconf/fslpython_install.sh"
        RUN bash -c "echo -ne '. ${FSLDIR}/etc/fslconf/fsl.sh; PATH+=:${FSLDIR}/bin\n\n' >> ~/.bashrc"
        RUN bash -c "cat ~/.bashrc"
        """.strip()

    if commands is not None:
        frag += "\n" + "\n".join(["""RUN bash -i -c '{}'""".format(command) for command in commands])

    if configure_ssh:

        if not distro.startswith(("ubuntu", "debian")):
            frag += "\n" + """
            RUN yes '' | sudo ssh-keygen -q -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
            """.strip()
        frag += "\n" + """
        # QC connection
        EXPOSE 8888

        RUN echo  X11UseLocalhost no | sudo tee --append /etc/ssh/sshd_config

        ENTRYPOINT bash -c 'sudo mkdir -p /run/sshd; sudo /usr/sbin/sshd; /bin/bash'
        """.strip()

    frag += "\n" + """
    RUN echo Finished
    """.strip()

    # We strip leading tab to have a more conventional docker file. We use tab to make the code more Human readable
    # each time we add multiline commands  the .strip function only remove the white space from the first line
    for x in frag.split('\n'):
        docker += x.lstrip() + '\n'

    if name is None:
        name = "sct-%s-%s" % (distro.replace(":", "-"), version)

    if not os.path.exists(name):
        os.makedirs(name)
    with io.open(os.path.join(name, "Dockerfile"), "wb") as f:
        f.write(docker.encode("utf-8"))

    if verbose:
        logger.info("You can now run: docker build -t %s %s", name, name)

    return name


if __name__ == "__main__":

    import argparse

    logger = logging.getLogger()
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)  # INFO)

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
                      default="ubuntu:18.04",
                      help="Distribution to use (docker image)",
                      required=True,
                      )

    subp.add_argument("--version",
                      default="4.0.0",
                      required=True,
                      )

    try:
        import argcomplete

        argcomplete.autocomplete(parser)
    except:
        pass

    args = parser.parse_args()

    if args.command == "generate":
        name = generate(distro=args.distro, version=args.version)
        print(name)
    else:
        parser.print_help(sys.stderr)
        raise SystemExit(1)

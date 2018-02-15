FROM ubuntu:16.04
MAINTAINER P-O Quirion <poq@criugm.qc.ca>

# Install dependencies available through apt-get
RUN apt-get update && apt-get install -y \
  git \
  wget \
  bzip2

RUN cd /opt && git clone --depth 1  https://github.com/neuropoly/spinalcordtoolbox.git

RUN cd /opt/spinalcordtoolbox && yes | ./install_sct 
RUN echo export PATH=${PATH}:/opt/spinalcordtoolbox/bin >>  /etc/bash.bashrc

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y  openssh-server xorg

RUN echo  X11UseLocalhost no  >> /etc/ssh/sshd_config
RUN useradd -ms /bin/bash sct
RUN echo "sct:sct" | chpasswd
EXPOSE 22

ADD ./start_servces.sh /sbin/start_servces.sh

ENTRYPOINT ["start_servces.sh"]

# To build the container: 
#  docker build --tag neuropoly/sct .

# To run the sct:
#  docker run -p 2222:22 --rm -it --name sct_ssh  neuropoly/sct 

# Then ssh to the contaner with X tunelling enable  option and the port to 2222 on the local host , you should then be 
# able to get images even on a window machine. 

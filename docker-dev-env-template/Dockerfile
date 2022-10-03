FROM daocloud.io/library/ubuntu:16.04

RUN apt-get update \
    && apt-get install -y apt-transport-https \
    && apt-get clean

RUN echo "deb http://mirrors.sjtug.sjtu.edu.cn/ubuntu/ xenial main restricted universe multiverse" > /etc/apt/sources.list \
    && echo "deb http://mirrors.sjtug.sjtu.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.sjtug.sjtu.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.sjtug.sjtu.edu.cn/ubuntu/ xenial-security main restricted universe multiverse" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y ssh sudo \
                          build-essential wget python unzip rsync bc cpio lib32z1 lib32ncurses5 lib32stdc++6 \
                          u-boot-tools texinfo zlib1g-dev liblzo2-dev uuid-dev pkg-config libncurses-dev \
                          asciidoc binutils bzip2 gawk gettext git libncurses5-dev libz-dev patch zlib1g-dev \
                          lib32gcc1 libc6-dev-i386 subversion flex uglifyjs git-core gcc-multilib p7zip p7zip-full \
                          msmtp libssl-dev  libglib2.0-dev xmlto qemu-utils upx libelf-dev autoconf automake \
                          libtool autopoint device-tree-compiler g++-multilib antlr3 gperf \
                          scons gcc-arm-none-eabi diffstat chrpath \
    && apt-get clean \
    && ln -sf bash /bin/sh
 
COPY gosu-amd64 /usr/local/bin/gosu
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY tmp/id_rsa.pub /authorized_keys
RUN chmod +x /usr/local/bin/gosu \
    && chmod a+x /usr/local/bin/docker-entrypoint.sh \
    && useradd --shell /bin/bash -c "" -m vagrant \
    && echo -n 'vagrant:vagrant' | chpasswd \
    && echo 'vagrant ALL = NOPASSWD: ALL' > /etc/sudoers.d/vagrant \
    && chmod 440 /etc/sudoers.d/vagrant \
    && mkdir -p /home/vagrant/.ssh \
    && chmod 700 /home/vagrant/.ssh \
    && mv /authorized_keys /home/vagrant/.ssh/authorized_keys \
    && chmod 600 /home/vagrant/.ssh/authorized_keys \
    && chown -R vagrant:vagrant /home/vagrant/.ssh \
    && sed -i -e 's/Defaults.*requiretty/#&/' /etc/sudoers \
    && sed -i -e 's/\(UsePAM \)yes/\1 no/' /etc/ssh/sshd_config

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]


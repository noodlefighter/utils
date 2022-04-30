# 同步回下载缓存
rsync -avl vagrant@ubuntu-xenial:/home/vagrant/yocto/downloads ../yocto

# 同步回构建好的文件
mkdir -p ../yocto/build
rsync -avl vagrant@ubuntu-xenial:/home/vagrant/yocto/build/tmp/deploy/images/mys6ull14x14 ../yocto/build/
rsync -avl vagrant@ubuntu-xenial:/home/vagrant/yocto/build/tmp/deploy/sdk ../yocto/build/
rsync -avl vagrant@ubuntu-xenial:/home/vagrant/yocto/build/tmp/work/cortexa7hf-neon-poky-linux-gnueabi/example/ ../yocto/build/example
rsync -avl vagrant@ubuntu-xenial:/home/vagrant/yocto/build/tmp/work/cortexa7hf-neon-poky-linux-gnueabi/device/ ../yocto/build/device

vagrant rsync

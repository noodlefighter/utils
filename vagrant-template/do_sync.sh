MYHOST=vagrant@ubuntu-focal
MYPATH=/home/vagrant/lede

# 同步回下载缓存
rsync -avl $MYHOST:$MYPATH/dl ./lede/dl

# 同步回构建好的文件
mkdir -p ./build
rsync -avl $MYHOST:$MYPATH/bin ./build/

# 为了执行vagrantfile内定义的rsync，似乎只能reload了，会导致机器重启
vagrant reload

# 
# 安装vagrant的scp插件：vagrant plugin install vagrant-scp
#

MYPATH=/home/vagrant/lede

# 同步回下载缓存
#vagrant scp :$MYPATH/dl ./lede/

# 同步回构建好的文件
mkdir -p ./bin
vagrant scp :$MYPATH/bin ./bin

vagrant rsync


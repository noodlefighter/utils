#!/bin/bash

USER_ID=${LOCAL_USER_ID:-9001}
#chown -R $USER_ID /workspaces

usermod -u $USER_ID vagrant
export HOME=/home/vagrant

service ssh start
exec /usr/local/bin/gosu vagrant "$@"


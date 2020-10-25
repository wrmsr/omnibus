#!/usr/bin/env bash
set -e

if [ "x$SSH_PASSWORD" == "x" ] ; then
    echo "Must set SSH_PASSWORD" >&2
    exit 1
fi

echo "root:$SSH_PASSWORD" | chpasswd
/usr/sbin/sshd -D

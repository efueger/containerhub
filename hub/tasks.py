# coding: utf-8

import os
import subprocess

from django.shortcuts import render
from celery import shared_task

from .models import Network


@shared_task()
def create_network(network: Network):
    """
    Creating a new bridge device on the host and activate it.

    :param network: the network that should be created
    :return:
    """
    with open('/etc/netctl/hubnet_%s' % network.uuid.hex) as f:
        config = 'Description="LXC bridge for hub network {uuid} of user {email}"\n' \
                 'Interface={interface}\n' \
                 'Connection=bridge\n' \
                 'BindsToInterfaces=()\n' \
                 'IP=static\n' \
                 'Address={address}\n' \
                 'SkipForwardingDelay=yes\n' \
                .format(uuid=str(network.uuid),
                        email=network.user.email,
                        interface='hubnet_%s' % network.uuid.hex,
                        address=network.network)
        f.write(config)
    args = ['sudo', 'netctl', 'enable', 'hubnet_%s' % network.uuid.hex]
    p = subprocess.Popen(args)
    os.system('netctl start hubnet_%s' % network.uuid.hex)


@shared_task()
def destroy_network(network: Network):
    """
    Remove a bridge device from the host system.
    **This should only be done if their are no hosts in the network**

    :param network: the netowkr that should be destroyed
    :return:
    """
    os.system('netctl stop hubnet_%s' % network.uuid.hex)
    os.system('netctl disable hubnet_%s' % network.uuid.hex)
    conf = '/etc/netctl/hubnet_%s' % network.uuid.hex
    if os.path.isfile(conf):
        os.unlink(conf)
    network.delete()

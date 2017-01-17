# coding: utf-8

import uuid
import random
import logging
import subprocess

from celery import shared_task
from django.conf import settings
from sshpubkeys import SSHKey
from sshpubkeys.exceptions import InvalidKeyException

from .models import Container, Network, IPAddress, SSHKey, Port


logger = logging.getLogger(__name__)


def online(container: uuid.UUID) -> bool:
    """
    Checks if a container is running or not.

    :param container:
    :return:
    """
    args = ['sudo', 'lxc-info', '-n', container.hex]
    p = subprocess.Popen(args)
    found = False
    for line in p.stdout.readlines():
        if line.startswith('State:'):
            found = True
            if not line.endswith('STOPPED'):
                return False

    if not found:
        return False
    else:
        return True

@shared_task()
def create_network(network: Network):
    """
    Creating a new bridge device on the host and activate it.

    :param network: the network that should be created
    :return:
    """
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

    args = ['sudo', 'netctl_helper', 'add', network.uuid.hex]
    p = subprocess.Popen(args, stdin=config)

    args = ['sudo', 'netctl', 'enable', 'hubnet_%s' % network.uuid.hex]
    p = subprocess.Popen(args)

    args = ['sudo', 'netctl', 'start', 'hubnet_%s' % network.uuid.hex]
    p = subprocess.Popen(args)


@shared_task()
def destroy_network(network: Network):
    """
    Remove a bridge device from the host system.
    **This should only be done if their are no hosts in the network**

    :param network: the netowkr that should be destroyed
    :return:
    """
    found = False
    for ip in network.ipaddress_set:
        if ip.container and online(ip.container):
            logger.error('Network still has running containers connected to it. Please shut them down before removing this network.')
            found = True

    if not found:
        args = ['sudo', 'netctl', 'stop', 'hubnet_%s' % network.uuid.hex]
        p = subprocess.Popen(args)

        args = ['sudo', 'netctl', 'disable', 'hubnet_%s' % network.uuid.hex]
        p = subprocess.Popen(args)

        args = ['sudo', 'netctl_helper', 'del', network.uuid.hex]
        p = subprocess.Popen(args)

        network.delete()


@shared_task()
def set_ipaddress(container: Container, network: Network, ipaddress: IPAddress):
    """
    Sets the IP configuration of a linux container.

    :param container: The container to update
    :param ipaddress: IP address as string
    :param netmask: Netmask as string.
    :param gateway: Gateway as string
    :return:
    """
    if not online(container.uuid):
        config = 'lxc.network.type=veth\n' \
                 'lxc.network.link=hubnet_{uuid}\n' \
                 'lxc.network.ipv4={ipaddress}\n' \
                 'lxc.network.ipv4.gateway={gateway}\n' \
                 'lxc.network.flags=up\n' \
                 'lxc.network.name=eth0\n' \
                 'lxc.network.mtu=1500\n' \
                 .format(uuid=network.uuid.hex,
                         ipaddress=ipaddress.ip,
                         gateway=network.gateway)
        args = ['sudo', 'lxc_helper', 'update', container.uuid.hex]
        p = subprocess.Popen(args, stdin=config)
        p.communicate()
        if p.returncode == 0:
            ipaddress.container = container
            ipaddress.save()
            # TODO: return success to user
            logger.info('IP address %s added to container %s' % (ipaddress.ip, str(container.uuid)))
    else:
        # TODO: return error to user
        logger.error('Container needs to be offline')


@shared_task()
def del_ipadress(container: uuid.UUID, ipaddress: IPAddress):
    """
    Removes an IP adsress from a container.

    :param container:
    :return:
    """
    if not online(container):
        args = ['sudo', 'lxc_helper', 'update', container.hex]
        p = subprocess.Popen(args)
        p.communicate()
        if p.returncode == 0:
            ipaddress.container = None
            ipaddress.save()
            # TODO: return success to user
            logger.info('IP address %s removed from container %s' % (ipaddress.ip, str(container)))
    else:
        # TODO: return error to user
        logger.error('Container needs to be offline')

@shared_task()
def add_sshkey(user: settings.AUTH_USER_MODEL, sshkey: str, comment: str = None):
    """
    Checks validity of ssh key and adds ot to user profile on success.

    :param user:
    :param sshkey:
    :return:
    """
    ssh = SSHKey(sshkey, strict_mode=True)
    try:
        ssh.parse()
        # TODO: show warning if users use Ecdsa (NIST) or DSA keys
        #if ssh.key_type not in ['ssh-rsa', 'ssh-ecdsa']:
        #    sshkey = '###invalid###%s' % 'Unsupported key type. Please use RSA or Ed25519 keys.'
        if not comment:
            comment = ssh.comment
    except InvalidKeyException as err:
        # TODO: make better error message, maybe based on the exception class
        sshkey = '###invalid###%s' % err.__doc__.strip()

    s = SSHKey(public_key=sshkey, comment=comment, user=user)
    s.save()


# TODO: this task should not be run multiple times at once. Ports could overwrite each other.
# http://docs.celeryproject.org/en/latest/tutorials/task-cookbook.html#ensuring-a-task-is-only-executed-one-at-a-time
@shared_task()
def get_port(container: Container, protocol: str, comment: str) -> int:
    """
    Select the next unused port and returns the port number.
    If the port table isn't filled yet it returns the highest unused port and adds it to the table. If the table is
    filled it returns a random port that is currently unused.

    The actual generation of port forwardings in the firewall is done by a cron job.

    :return:
    """
    ports = Port.objects.count()
    if ports < 65535 - 10000:
        port = Port(container=container, port=ports, protocol=protocol, comment=comment)
        port.save()
    else:
        port = random.choice(Port.objects.filter(container=None).all())
        port.container = container
        port.protocol = protocol
        port.comment = comment
        port.save()

    return port.port

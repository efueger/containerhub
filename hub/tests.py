# coding: utf-8

from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from .models import Container, Network, IPAddress, Domain, Port, SSHKey, PROTOCOL_CHOICES
from .tasks import create_network, destroy_network


# Create your tests here.

def create_container(name, user, template=None):
    """
    creates a container

    :return:
    """
    if not template:
        # TODO: replace with actual template name
        template = 'debian'
    return Container.objects.create(name=name, owner=user, template=template)


class ContainerTests(TestCase):

    def setUp(self):
        # TODO: create better test data
        self.user = settings.AUTH_USER_MODEL.objects.create_user(username='rick', email='rick@example.com', password='top_secret')

    def test_creation_dates(self):
        """
        check if creation date and modification date is set correctly

        :return:
        """
        now = timezone.now()
        # TODO: generate random name
        container = create_container(name='testcontainer', user=self.user)
        then = timezone.now()

        self.assertIs(now < container.created)
        self.assertIs(container.created < then)

        self.assertIs(now < container.modified)
        self.assertIs(container.modified < then)


class ContainerMethodTests(TestCase):

    def setUp(self):
        # TODO: create better test data
        self.user = settings.AUTH_USER_MODEL.objects.create_user(username='rick', email='rick@example.com', password='top_secret')

    def test_sshconfig(self):
        """
        check if sshconfig is correctly generated
        :return:
        """
        # TODO: generate random name
        name = 'testcontainer'

        container = create_container(name=name, user=self.user)
        sshconfig = container.sshconfig()
        lines = sshconfig.split('\n')

        self.assertIs(lines[0], 'Host %s' % name)
        self.assertIn('    HostName %s' % settings.HOST_IP, lines[1:])
        self.assertIn('    #Port', lines[1:])
        self.assertIn('    User root', lines[1:])
        self.assertIn('    IdentitiesOnly yes', lines[1:])
        self.assertIn('    IdentityFile ~/.ssh/id_rsa', lines[1:])

        # TODO: add network and check if port is in sshconfig


class NetworkTests(TestCase):
    pass


class IPAddressTests(TestCase):
    pass


class DomainTests(TestCase):
    pass


class PortTests(TestCase):
    pass


class SSHKeyTests(TestCase):
    pass

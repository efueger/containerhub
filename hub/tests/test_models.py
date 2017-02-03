import uuid

import pytest
from django.conf import settings
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestProfile:
    TEST_USERNAME = 'luke'
    TEST_EMAIL = 'luke@skywalker.com'

    def test_model(self):
        # Profiles are only generated when users are created
        obj = mixer.blend('auth.User', username=self.TEST_USERNAME, email=self.TEST_EMAIL)

        assert obj.pk == 1, 'Should create a User instance'
        assert obj.profile.pk == 1, 'Should create a Profile instance'
        assert str(obj.profile) == '%s <%s>' % (self.TEST_USERNAME, self.TEST_EMAIL)


class TestSSHKey:
    def test_model(self):
        obj = mixer.blend('hub.SSHKey')

        assert obj.pk == 1, 'Should create a SSHKey instance'


class TestContainer:
    def test_model(self):
        obj = mixer.blend('hub.Container', uuid=uuid.uuid4())

        assert obj.pk == 1, 'Should create a Container instance'

        config = f'Host {obj.name}\n' \
                 f'    HostName {settings.HOST_IP}\n' \
                 '    #Port\n' \
                 '    User root\n' \
                 '    IdentitiesOnly yes\n' \
                 '    IdentityFile ~/.ssh/id_rsa'

        assert obj.sshconfig() == config

        port = mixer.blend('hub.Port', comment='SSH', container=obj)
        config = f'Host {obj.name}\n' \
                 f'    HostName {settings.HOST_IP}\n' \
                 f"    Port {port.port}\n" \
                 '    User root\n' \
                 '    IdentitiesOnly yes\n' \
                 '    IdentityFile ~/.ssh/id_rsa'

        assert obj.sshconfig() == config


class TestPort:
    def test_model(self):
        con = mixer.blend('hub.Container', uuid=uuid.uuid4())
        obj = mixer.blend('hub.Port', container=con)

        assert obj.pk == 1, 'Should create a Port instance'


class TestNetwork:
    def test_model(self):
        obj = mixer.blend('hub.Network', uuid=uuid.uuid4())

        assert obj.pk == 1, 'Should create a Network instance'


class TestIPAddress:
    def test_model(self):
        net = mixer.blend('hub.Network', uuid=uuid.uuid4())
        con = mixer.blend('hub.Container', uuid=uuid.uuid4())
        obj = mixer.blend('hub.IPAddress', network=net, container=con)

        assert obj.pk == 1, 'Should create a IPAddress instance'


class TestDomain:
    def test_model(self):
        obj = mixer.blend('hub.Domain')

        assert obj.pk == 1, 'Should create a Domain instance'

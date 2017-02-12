import os
import uuid
import shlex
import subprocess
from shutil import rmtree
from tempfile import mkdtemp

import pytest
import sshpubkeys
from django.conf import settings
from mixer.backend.django import mixer


pytestmark = pytest.mark.django_db

TEST_USERNAME = 'luke'
TEST_EMAIL = 'luke@skywalker.com'


class TestProfile:
    def test_model(self):
        # Profiles are only generated when users are created
        obj = mixer.blend('auth.User', username=TEST_USERNAME, email=TEST_EMAIL)

        assert obj.pk == 1, 'Should create a User instance'
        assert obj.profile.pk == 1, 'Should create a Profile instance'
        assert str(obj.profile) == '%s <%s>' % (TEST_USERNAME, TEST_EMAIL)


class TestSSHKey:
    def test_model(self, tmpdir):
        def ssh_keygen(b: int = 4096, t: str = 'rsa', comment: str = 'some comment') -> str:
            """
            Generate an openssh keypair and return the public key as plaintext.

            :param b: key size in bytes
            :param t: key type, can be 'rsa', 'ecdsa' or 'ed25519'
            :param comment: key comment
            :return: the public key as string
            """
            keyfile = os.path.join(testdir, f'id_{t}_{uuid.uuid4()}')
            pubkeyfile = f'{keyfile}.pub'
            args = f'ssh-keygen -q -b {b} -t {t} -N "" -C "{comment}" -f {keyfile}'
            subprocess.call(shlex.split(args))
            with open(pubkeyfile) as fh:
                return fh.read()

        testdir = mkdtemp(prefix='hub')
        rsa_4096_raw = ssh_keygen(4096, 'rsa', 'rsa 4096')
        rsa_2048_raw = ssh_keygen(2048, 'rsa', 'rsa 4096')
        ecdsa_256_raw = ssh_keygen(256, 'ecdsa', 'ecdsa 256')
        ed25519_256_raw = ssh_keygen(256, 'ed25519', 'ed25519 256')


        user = mixer.blend('auth.User', username=TEST_USERNAME, email=TEST_EMAIL)
        rsa_4096_obj = mixer.blend('hub.SSHKey', user=user, public_key=rsa_4096_raw)
        rsa_2048_obj = mixer.blend('hub.SSHKey', user=user, public_key=rsa_2048_raw)
        ecdsa_256_obj = mixer.blend('hub.SSHKey', user=user, public_key=ecdsa_256_raw)
        ed25519_256_obj = mixer.blend('hub.SSHKey', user=user, public_key=ed25519_256_raw)

        assert rsa_4096_obj.pk == 1, 'Should create a SSHKey instance'
        assert rsa_2048_obj.pk == 2, 'Should create a SSHKey instance'
        assert ecdsa_256_obj.pk == 3, 'Should create a SSHKey instance'
        assert ed25519_256_obj.pk == 4, 'Should create a SSHKey instance'

        assert rsa_4096_obj.user.username == user.username
        assert rsa_4096_obj.user.email == user.email
        assert rsa_4096_obj.public_key == rsa_4096_raw
        assert str(rsa_4096_obj) == sshpubkeys.SSHKey(keydata=rsa_4096_raw).hash_sha512()

        assert rsa_2048_obj.user.username == user.username
        assert rsa_2048_obj.user.email == user.email
        assert rsa_2048_obj.public_key == rsa_2048_raw
        assert str(rsa_2048_obj) == sshpubkeys.SSHKey(keydata=rsa_2048_raw).hash_sha512()

        assert ecdsa_256_obj.user.username == user.username
        assert ecdsa_256_obj.user.email == user.email
        assert ecdsa_256_obj.public_key == ecdsa_256_raw
        assert str(ecdsa_256_obj) == sshpubkeys.SSHKey(keydata=ecdsa_256_raw).hash_sha512()

        assert ed25519_256_obj.user.username == user.username
        assert ed25519_256_obj.user.email == user.email
        assert ed25519_256_obj.public_key == ed25519_256_raw
        assert str(ed25519_256_obj) == sshpubkeys.SSHKey(keydata=ed25519_256_raw).hash_sha512()

        rmtree(testdir, ignore_errors=True)


class TestContainer:
    TEST_NAME = 'mycontainer'
    TEST_TEMPLATE = 'archlinux'

    def test_model(self):
        obj = mixer.blend('hub.Container', uuid=uuid.uuid4(), name=self.TEST_NAME, template=self.TEST_TEMPLATE)

        assert obj.pk == 1, 'Should create a Container instance'
        assert str(obj) == f'{self.TEST_NAME} ({self.TEST_TEMPLATE})'

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

        # NOTE: this test could be applied to all models.
        before = obj.modified
        obj.name = f'{self.TEST_NAME}_'
        obj.save()
        after = obj.modified
        assert before < after


class TestPort:
    def test_model(self):
        con = mixer.blend('hub.Container', uuid=uuid.uuid4())
        obj = mixer.blend('hub.Port', container=con)

        assert obj.pk == 1, 'Should create a Port instance'
        assert obj.port > 10000
        assert obj.port < 65535
        obj2 = mixer.blend('hub.Port', container=con, port=100)


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

import sshpubkeys
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from .choices import PROTOCOL_CHOICES


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    c_base_uid = models.PositiveIntegerField(blank=True, null=True)
    verified = models.BooleanField(default=False)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f'{self.user.username} <{self.user.email}>'

    class Meta:
        ordering = ('user', )


class SSHKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    public_key = models.CharField(max_length=4096)

    def __str__(self):
        s = sshpubkeys.SSHKey(keydata=self.public_key)
        return s.hash_sha512()
        #return f'{self.public_key[:32]}... ({self.comment})'


class Container(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    template = models.CharField(max_length=255)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.template})'

    def sshconfig(self):
        """
        Generates ssh config to connect to this container
        """
        config = f'Host {self.name}\n' \
                 f'    HostName {settings.HOST_IP}\n'
        port = self.ports.filter(comment='SSH').first()
        if port:
            # TODO: find SSH port
            config += f'    Port {port.port}\n'
        else:
            config += '    #Port\n'
        config += '    User root\n' \
                  '    IdentitiesOnly yes\n' \
                  '    IdentityFile ~/.ssh/id_rsa'
        return config

    class Meta:
        ordering = ('owner', 'name')


class Port(models.Model):
    comment = models.CharField(max_length=255, blank=True, null=True)
    port = models.PositiveIntegerField(validators=[MinValueValidator(10000, 'Minimum port number is 10000'), MaxValueValidator(65535, 'Maximum port number is 65535')])
    protocol = models.PositiveSmallIntegerField(choices=PROTOCOL_CHOICES, default=1)  # default: TCP
    # TODO: on_delete is probably not correct
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='ports', null=True)

    def __str__(self):
        return f'{self.port} ({self.get_protocol_display()})'

    class Meta:
        ordering = ('container', 'port')


class Network(models.Model):
    uuid = models.UUIDField(unique=True)
    network = models.GenericIPAddressField()
    subnet = models.PositiveSmallIntegerField()
    gateway = models.GenericIPAddressField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.network}/{self.subnet} -> {self.gateway}'


class IPAddress(models.Model):
    ip = models.GenericIPAddressField()
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    container = models.ForeignKey(Container, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.container:
            return f'{self.ip}/{self.network.subnet} ({self.container.name})'
        else:
            return f'{self.ip}/{self.network.subnet}'


class Domain(models.Model):
    name = models.CharField(max_length=255)
    ip = models.ForeignKey(IPAddress, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} -> {self.ip.ip}'

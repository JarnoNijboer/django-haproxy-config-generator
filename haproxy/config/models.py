from django.db import models


class Customer(models.Model):
    name = models.CharField('Customer', max_length=100)
    slug = models.CharField('Slug', max_length=32)

    def __unicode__(self):
        return self.name


class Site(models.Model):
    MODES = (
        ('tcp', 'TCP'),
        ('http', 'HTTP')
    )

    DEFAULT_MODE = 'http'

    mode = models.CharField('Mode', choices=MODES, max_length=4, default=DEFAULT_MODE)
    customer = models.ForeignKey('Customer')
    enabled = models.BooleanField('Enabled', default=True)

    enable_http = models.BooleanField('Enable HTTP', default=True)

    enable_https = models.BooleanField('Enable HTTPS', default=True)
    force_https = models.BooleanField('Force HTTPS', default=True)
    enable_sts = models.BooleanField('Enable STS', default=True)
    enable_letsencrypt = models.BooleanField('Enable LetsEncrypt', default=True)

    custom_configs = models.TextField('Custom backend config', null=True, blank=True)

    @property
    def enabled_domains(self):
        return self.domain_list.filter(enabled=True)

    def __unicode__(self):
        desc = self.enabled_domains[0].domain
        if self.enabled_domains.count() > 1:
            desc = "{} and {} others".format(desc, self.enabled_domains.count() - 1)
        return desc


class Domain(models.Model):
    site = models.ForeignKey('Site', on_delete=models.CASCADE, related_name='domain_list')
    domain = models.CharField('Domain', max_length=100)
    enabled = models.BooleanField('Enabled', default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.domain


class Server(models.Model):
    site = models.ForeignKey('Site')
    name = models.CharField('Server name', max_length=100, default='app')
    address = models.CharField('Server address', max_length=100)
    check = models.BooleanField('Check', default=True)

    def __unicode__(self):
        return "{} ({})".format(self.name, self.address)

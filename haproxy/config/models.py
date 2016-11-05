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

    customer = models.ForeignKey('Customer')
    main_domain = models.CharField('Main domain', max_length=100)

    mode = models.CharField('Mode', choices=MODES, max_length=4)

    enable_http = models.BooleanField('Enable HTTP', default=True)

    enable_https = models.BooleanField('Enable HTTPS', default=True)
    force_https = models.BooleanField('Force HTTPS', default=True)
    enable_sts = models.BooleanField('Enable STS', default=True)
    enable_letsencrypt = models.BooleanField('Enable LetsEncrypt', default=True)

    custom_configs = models.TextField('Custom backend config', null=True, blank=True)

    def __unicode__(self):
        return self.main_domain


class Domain(models.Model):
    site = models.ForeignKey('Site')
    domain = models.CharField('Domain', max_length=100)

    def __unicode__(self):
        return "{} ({})".format(self.domain, self.site)


class Server(models.Model):
    site = models.ForeignKey('Site')
    name = models.CharField('Server name', max_length=100, default='app')
    address = models.CharField('Server address', max_length=100)
    check = models.BooleanField('Check', default=True)

    def __unicode__(self):
        return "{} ({})".format(self.name, self.address)

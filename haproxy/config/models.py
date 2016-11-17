from django.db import models

class Site(models.Model):
    MODES = (
        ('tcp', 'TCP'),
        ('http', 'HTTP')
    )

    DEFAULT_MODE = 'http'

    mode = models.CharField('Mode', choices=MODES, max_length=4, default=DEFAULT_MODE)
    enabled = models.BooleanField('Enabled', default=True)

    enable_http = models.BooleanField(
        'Enable HTTP', default=True,
        help_text='Enables the site to be served on the HTTP frontend.')
    enable_https = models.BooleanField(
        'Enable HTTPS', default=True,
        help_text='Enables the site to be served on the HTTPS frontend.')
    force_https = models.BooleanField(
        'Force HTTPS', default=True,
        help_text='Redirects the user to the HTTPS website when enabled.')
    enable_sts = models.BooleanField(
        'Enable STS', default=True,
        help_text='Security measurement. This will force browsers to use HTTPS on this site.')
    enable_letsencrypt = models.BooleanField(
        'Enable LetsEncrypt', default=True,
        help_text='HTTP and HTTP mode must be enabled for this site in order for LetsEncrypt to work.')

    custom_configs = models.TextField('Custom backend config', null=True, blank=True)

    @property
    def enabled_domains(self):
        return self.domain_list.filter(enabled=True)

    @property
    def backend_config(self):
        config = ['mode %s' % self.mode]

        if self.enable_letsencrypt:
            # Execute LetsEncrypt acme-http01 lua script if the requested path is something like
            # .well-known/acme-challenge/, the request method is GET and the request is over HTTP.
            config.append('acl url_acme_http01 path_beg /.well-known/acme-challenge/')
            config.append('http-request use-service lua.acme-http01 if !{ ssl_fc } METH_GET url_acme_http01')

        if self.force_https:
            # Redirect to the HTTPS scheme when requested over HTTP.
            config.append('redirect scheme https if !{ ssl_fc }')

        if self.enable_sts:
            # Add the Strict-Transport-Security header (age is 7 days)
            config.append('rspadd Strict-Transport-Security:\ max-age=15552000')

        if self.mode == 'http':
            # Add an X-Forwarded-For header at the server-side if this backend is in HTTP mode
            config.append('option forwardfor')

        if self.custom_configs:
            # Add custom configs if they're given
            config.append('')
            config.append('# START custom config')
            config.append(str(self.custom_configs))
            config.append('# END custom config')
            config.append('')

        for server in self.server_list.all():
            # Add all the backend servers
            config.append(server.server_config)

        return '\n    '.join(config)

    def __unicode__(self):
        desc = self.enabled_domains[0].domain
        if self.enabled_domains.count() > 1:
            desc = "{} and {} others".format(desc, self.enabled_domains.count() - 1)
        return desc


class Domain(models.Model):
    site = models.ForeignKey('Site', on_delete=models.CASCADE, related_name='domain_list')
    domain = models.CharField('Domain', max_length=100)
    exact = models.BooleanField('Exact', default=True)
    enabled = models.BooleanField('Enabled', default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.domain


class Server(models.Model):
    site = models.ForeignKey('Site', on_delete=models.CASCADE, related_name='server_list')
    name = models.CharField('Server name', max_length=100, default='app')
    address = models.CharField('Server address', max_length=100)
    check = models.BooleanField('Check', default=True)

    @property
    def server_config(self):
        if self.check:
            return 'server %s %s check' % (self.name, self.address)
        else:
            return 'server %s %s' % (self.name, self.address)

    def __unicode__(self):
        return "{} ({})".format(self.name, self.address)

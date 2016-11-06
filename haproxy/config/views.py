from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from config.models import Site


@login_required()
def print_config(_):
    sites = Site.objects.filter(enabled=True).select_related('customer')

    def get_frontend(filter_, exact_if, non_exact_if):
        for site in sites.filter(**filter_):
            for domain in site.enabled_domains:
                yield 'use_backend bk_%s_%d if { %s -i %s }' % (
                    site.customer.slug, site.id, (exact_if if domain.exact else non_exact_if), domain.domain)

    return render_to_response(
        'config.tpl',
        context={
            'http_frontend': '\n    '.join(get_frontend({'enable_http': True}, 'hdr(host)', 'hdr_end(host)')),
            'https_frontend': '\n    '.join(get_frontend({'enable_https': True}, 'ssl_fc_sni', 'ssl_fc_sni_end')),
            'sites': sites,
        },
        content_type='text/plain')

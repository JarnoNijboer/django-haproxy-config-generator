from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from config.models import Site


@login_required()
def print_config(_):
    return render_to_response(
        'config.tpl',
        context={'sites': Site.objects.all()},
        content_type='text/plain')

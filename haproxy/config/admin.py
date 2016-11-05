from django.contrib import admin
from models import Customer, Site


class SiteAdmin(admin.ModelAdmin):
    list_display = ('main_domain', 'customer', 'mode', 'enable_http', 'enable_https',)
    fieldsets = (
        (None, {
            'fields': ('customer', 'mode', 'main_domain',)
        }),
        ('HTTP settings', {
            'fields': ('enable_http',),
        }),
        ('HTTPS settings', {
            'fields': ('enable_https', 'force_https', 'enable_sts', 'enable_letsencrypt',),
        }),
    )

admin.site.register(Site, SiteAdmin)
admin.site.register(Customer)

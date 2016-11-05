from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from models import Customer, Site, Domain


class DomainListInline(InlineModelAdmin):
    template = 'admin/InlineWithoutOriginal.html'
    model = Domain
    fields = ('domain', 'created', 'enabled',)
    readonly_fields = ('created',)
    can_delete = True
    extra = 1
    ordering = ('id',)
    original = False


class SiteAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'customer', 'enabled', 'mode', 'enable_http', 'enable_https',)
    fieldsets = (
        (None, {
            'fields': ('mode', 'customer', 'enabled',)
        }),
        ('HTTP settings', {
            'fields': ('enable_http',),
        }),
        ('HTTPS settings', {
            'fields': ('enable_https', 'force_https', 'enable_sts', 'enable_letsencrypt',),
        }),
        ('Custom backend configuration', {
            'classes': ('collapse',),
            'fields': ('custom_configs',),
        }),
    )
    inlines = [DomainListInline]

admin.site.register(Site, SiteAdmin)
admin.site.register(Customer)

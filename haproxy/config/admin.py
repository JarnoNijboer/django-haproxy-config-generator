from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from models import Customer, Site, Domain, Server


class BaseConfigInline(InlineModelAdmin):
    template = 'admin/InlineWithoutOriginal.html'
    can_delete = True
    extra = 1
    ordering = ('id',)


class DomainListInline(BaseConfigInline):
    model = Domain
    fields = ('domain', 'created', 'enabled',)
    readonly_fields = ('created',)


class ServerListInline(BaseConfigInline):
    model = Server
    fields = ('name', 'address', 'check',)


class SiteAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'customer', 'enabled', 'mode', 'enable_http', 'enable_https',)
    list_filter = ('customer', 'enabled', 'mode', 'enable_http', 'enable_https',)
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
    inlines = [DomainListInline, ServerListInline]

admin.site.register(Site, SiteAdmin)
admin.site.register(Customer)

from django_hosts import patterns, host
from django.conf import settings

host_patterns = patterns(
    '',
    host(r'', settings.ROOT_URLCONF, name='app'),
    host('api', 'external.api_urls', name='api'),
    host('ioadmin', 'users.urls_admin', name="admin"),
    host('panel', 'users.urls', name="user-area"),

    host('api-staging', 'external.api_urls', name='api-staging'),
    host('ioadmin-staging', 'users.urls_admin', name="admin-staging"),
    host('panel-staging', 'users.urls', name="user-area-staging"),

    host('do-api', 'external.api_urls', name='api-digital-ocean'),
    host('admin', 'users.urls_admin', name='admin-digital-ocean'),
    host('do', 'users.urls', name='panel-digital-ocean'),
)

global
    log-tag                     haproxy
    log                         127.0.0.1 local0 notice
    chroot                      /var/lib/haproxy
    pidfile                     /var/run/haproxy.pid
    stats socket                /var/lib/haproxy/stats
    maxconn                     4096
    tune.bufsize                16384
    tune.maxrewrite             1024
    tune.ssl.maxrecord          1400
    tune.ssl.default-dh-param   4096
    lua-load                    /etc/haproxy/certs/acme-http01-webroot.lua
    ssl-default-bind-ciphers    ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS
    ssl-default-bind-options    no-sslv3
    daemon

defaults
    log                         global
    option                      dontlognull
    option                      redispatch
    option                      http-server-close
    retries                     3
    timeout check               2s
    timeout connect             5s
    timeout http-request        10s
    timeout client              10s
    timeout server              30s
    timeout http-keep-alive     120s
    errorfile 503               /etc/haproxy/errors/503.http

frontend http_in
    bind *:80
    mode http

    option httplog

    {{ http_frontend }}

    default_backend {{ http_default_backend }}

frontend https_in
    bind *:443 ssl crt /etc/haproxy/certs/live/ npn http/1.1,http/1.0
    mode tcp

    option tcplog

    # Require SSL handshakes within 5 seconds
    tcp-request inspect-delay 5s
    tcp-request content accept if { req.ssl_hello_type 1 }

    # Reset default timeouts on the frontend to allow Outlook Anywhere (RPC-over-HTTP) sessions
    # Backends will extend from the defaults in order to keep long connects out after all
    timeout http-request    12h
    timeout client          12h
    timeout http-keep-alive 12h

    {{ https_frontend }}

    default_backend {{ https_default_backend }}

{% if stats %}
frontend stats_in
    bind *:8000
    mode http

    stats                       enable
    stats auth                  {{ stats_username }}:{{ stats_password }}
    stats uri                   {{ stats_path }}
    stats refresh               {{ stats_refresh }}s

    default_backend {{ http_default_backend }}
{% endif %}

{% for site in sites %}
# {{ site.id }}: {{ site }}
backend bk_{{ site.id }}
    {{ site.backend_config }}

{% endfor %}

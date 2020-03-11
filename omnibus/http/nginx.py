"""
daemon off;
worker_processes 1;
error_log /dev/null;
pid {os.path.join(ng.temp_path, 'nginx.pid')};

events {{
  worker_connections 8;
  accept_mutex off;
}}

http {{
  charset utf-8;
  vhost_traffic_status_zone;

  upstream backend {{
    server unix:scgi.sock fail_timeout=0;
  }}

  server {{
    access_log off;
    listen {port} backlog=1;

    location /nginx {{
      add_header Content-Type text/plain;
      return 200 '';
    }}

    location /nginx/status {{
      stub_status on;
      access_log off;
    }}

    {ng.temp_subdirs_config_block}

    location /nginx/vts {{
      vhost_traffic_status_display;
      vhost_traffic_status_display_format html;
    }}

    location / {{

      scgi_param REQUEST_METHOD $request_method;
      scgi_param REQUEST_URI $request_uri;
      scgi_param QUERY_STRING $query_string;
      scgi_param CONTENT_TYPE $content_type;

      scgi_param DOCUMENT_URI $document_uri;
      scgi_param DOCUMENT_ROOT $document_root;
      scgi_param SCGI 1;
      scgi_param SERVER_PROTOCOL $server_protocol;
      scgi_param REQUEST_SCHEME $scheme;
      scgi_param HTTPS $https if_not_empty;

      scgi_param REMOTE_ADDR $remote_addr;
      scgi_param REMOTE_PORT $remote_port;
      scgi_param SERVER_PORT $server_port;
      scgi_param SERVER_NAME $server_name;

      scgi_pass backend;
    }}
  }}
}}
"""
from . import lang


lang.warn_unstable()

"""
TODO:
 - streaming vts relay endpoint

###

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
import shlex
import subprocess
import typing as ta

from .. import configs
from .. import dataclasses as dc
from .. import properties


class ConfigItem(dc.Pure):
    value: str
    block: ta.Optional['ConfigItems'] = None

    @classmethod
    def of(cls, *args) -> 'ConfigItem':
        if len(args) == 1:
            [arg] = args
            if isinstance(arg, cls):
                return arg
            elif isinstance(arg, str):
                return cls(arg)
        elif len(args) == 2:
            arg0, arg1 = args
            if isinstance(arg0, str):
                if arg1 is None:
                    return cls(arg0, arg1)
                else:
                    return cls(arg1, ConfigItems.of(arg1))
        raise TypeError(args)


class ConfigItems(dc.Pure):
    items: ta.Sequence[ConfigItem]

    @classmethod
    def of(cls, arg) -> 'ConfigItems':
        if isinstance(arg, cls):
            return arg
        elif isinstance(arg, ta.Iterable):
            return cls(list(map(ConfigItem.of, arg)))
        else:
            raise TypeError(arg)


class NginxProcess(configs.Configurable):

    class Config(configs.Config):

        connect_timeout = 75.
        send_timeout = 15.
        read_timeout = 5.

    def __init__(self, config: Config = Config()) -> None:
        super().__init__(config)

    @properties.cached
    def nginx_exe(self) -> str:
        return 'nginx'

    @properties.cached
    def nginx_info(self) -> str:
        (_, stderr) = subprocess.Popen([self.nginx_exe, '-V'], stderr=subprocess.PIPE).communicate()
        return stderr.decode('utf-8').strip()

    @properties.cached
    def nginx_version_str(self) -> ta.Optional[str]:
        for line in self.nginx_info.split('\n'):
            if line.startswith('nginx version: '):
                ver = line.partition(': ')[2]
                if ' ' in ver:
                    ver = ver.partition(' ')[0]
                if ver.startswith('nginx/'):
                    ver = ver.partition('/')[2]
                return ver
        return None

    @properties.cached
    def nginx_version(self) -> ta.Optional[ta.Sequence[int]]:
        if self.nginx_version_str is not None:
            return tuple(map(int, self.nginx_version_str.split('.')))
        else:
            return None

    @properties.cached
    def nginx_cfg_args(self) -> ta.Optional[ta.List[str]]:
        for line in self.nginx_info.split('\n'):
            if line.startswith('configure arguments: '):
                cfg_line = line.partition(': ')[2]
                return shlex.split(cfg_line)
        return None

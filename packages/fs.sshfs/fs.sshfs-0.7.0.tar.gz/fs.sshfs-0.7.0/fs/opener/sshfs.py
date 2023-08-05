# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import configparser

from .base import Opener
from ..subfs import ClosingSubFS

__license__ = "LGPL-2.1+"
__copyright__ = "Copyright (c) 2017 Martin Larralde"
__author__ = "Martin Larralde <martin.larralde@ens-cachan.fr>"
__version__ = 'dev'


# Dynamically get the version of the main module
try:
    _name = __name__.replace('.opener', '')
    import pkg_resources
    __version__ = pkg_resources.get_distribution(_name).version
except Exception: # pragma: no cover
    pkg_resources = None
finally:
    del pkg_resources


class SSHOpener(Opener):
    protocols = ['ssh']

    @staticmethod
    def open_fs(fs_url, parse_result, writeable, create, cwd):
        from ..sshfs import SSHFS
        ssh_host, _, dir_path = parse_result.resource.partition('/')
        ssh_host, _, ssh_port = ssh_host.partition(':')
        ssh_port = int(ssh_port) if ssh_port.isdigit() else 22

        params = configparser.ConfigParser()
        params.read_dict({'sshfs':getattr(parse_result, 'params', {})})

        ssh_fs = SSHFS(
            ssh_host,
            port=ssh_port,
            user=parse_result.username,
            passwd=parse_result.password,
            pkey=params.get('sshfs', 'pkey', fallback=None),
            timeout=params.getint('sshfs', 'timeout', fallback=10),
            keepalive=params.getint('sshfs', 'keepalive', fallback=10),
            compress=params.getboolean('sshfs', 'compress', fallback=False),
            config_path=\
                params.get('sshfs', 'config_path', fallback='~/.ssh/config')
        )

        if dir_path: # pragma: no cover
            return ssh_fs.opendir(dir_path, factory=ClosingSubFS)
        else:
            return ssh_fs

#!/usr/bin/python3
"""script that distributes an archive to your web servers"""
from fabric.api import *
from datetime import datetime
import os
env.hosts = ["3.80.18.6", "3.84.238.206"]
env.user = 'ubuntu'


def do_pack():
    """generates a .tgz archive from the contents"""
    try:
        local('mkdir -p versions')
        date_format = '%Y%m%d%H%M%S'
        arch_path = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime(date_format))
        local('tar -cvzf {} web_static'.format(arch_path))
        print('web_static packed: {} -> {}'.format(arch_path,
              os.path.getsize(arch_path)))
    except TypeError:
        return None


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False
    f_name = archive_path.split('/')[1]
    f_path = '/data/web_static/releases/'
    r_path = f_path + f_name[:-4]
    try:
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(r_path))
        run('tar -xzf /tmp/{} -C {}'.format(f_name, r_path))
        run('rm /tmp/{}'.format(f_name))
        run('mv {}/web_static/* {}/'.format(r_path, r_path))
        run('rm -rf {}/web_static'.format(r_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(r_path))
        print('New version deployed!')
        return True
    except TypeError:
        return False
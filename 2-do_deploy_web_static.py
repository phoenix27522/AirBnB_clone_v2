#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import local, env, put, run
from os import path

env.hosts = ["3.80.18.6", "3.84.238.206"]


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, "/tmp/")

        # Extract the archive to /data/web_static/releases/<archive_filename without extension>
        archive_filename = archive_path.split("/")[-1]
        archive_folder = "/data/web_static/releases/{}".format(
            archive_filename.split(".")[0])
        run("mkdir -p {}".format(archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, archive_folder))

        # Remove the uploaded archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Create a symbolic link /data/web_static/current pointing to the new version
        run("rm -f /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(archive_folder))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed:", str(e))
        return False

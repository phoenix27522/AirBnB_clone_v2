#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run, sudo

env.hosts = ["3.80.18.6", "3.84.238.206"]


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        print("Error: Archive file does not exist.")
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    print("Running command: put({}, /tmp/{})".format(archive_path, file))
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        print("Error: Failed to upload the archive.")
        return False

    print("Running command: sudo rm -rf /data/web_static/releases/{}/".format(name))
    if sudo("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
        print("Error: Failed to remove existing release directory.")
        return False

    print("Running command: sudo mkdir -p /data/web_static/releases/{}/".format(name))
    if sudo("mkdir -p /data/web_static/releases/{}/".format(name)).failed is True:
        print("Error: Failed to create release directory.")
        return False

    print("Running command: sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name))
    if sudo("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed is True:
        print("Error: Failed to extract archive.")
        return False

    print("Running command: sudo rm /tmp/{}".format(file))
    if sudo("rm /tmp/{}".format(file)).failed is True:
        print("Error: Failed to remove temporary archive.")
        return False

    print("Running command: sudo mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name))
    if sudo("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed is True:
        print("Error: Failed to move files within the release directory.")
        return False

    print("Running command: sudo rm -rf /data/web_static/releases/{}/web_static".format(name))
    if sudo("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed is True:
        print("Error: Failed to remove redundant web_static directory.")
        return False

    print("Running command: sudo rm -rf /data/web_static/current")
    if sudo("rm -rf /data/web_static/current").failed is True:
        print("Error: Failed to remove current symbolic link.")
        return False

    print("Running command: sudo ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))
    if sudo("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed is True:
        print("Error: Failed to create new symbolic link.")
        return False

    print("Deployment successful.")
    return True

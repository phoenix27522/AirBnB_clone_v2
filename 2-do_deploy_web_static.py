from fabric.api import env, put, run
from fabric.contrib.files import exists

env.hosts = ["104.196.168.90", "35.196.46.172"]

def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not exists(archive_path):
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    put_result = put(archive_path, "/tmp/{}".format(file))
    if put_result.failed:
        return False

    run("rm -rf /data/web_static/releases/{}/".format(name))
    run("mkdir -p /data/web_static/releases/{}/".format(name))
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name))
    run("rm /tmp/{}".format(file))
    run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name))
    run("rm -rf /data/web_static/releases/{}/web_static".format(name))
    run("rm -rf /data/web_static/current")
    run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))

    return True

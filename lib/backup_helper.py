import tarfile
from datetime import datetime
from os import path, getenv, remove
import sh

directories = ['.screenly', 'screenly_assets']
static_dir = "screenly/static"


def create_backup(name="screenly"):
    home = getenv('HOME')
    archive_name = "{}-{}.tar.gz".format(
        name if name else 'screenly-backup',
        datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    )
    file_path = path.join(home, static_dir, archive_name)
    if path.isfile(file_path):
        remove(file_path)

    try:
        with tarfile.open(file_path, "w:gz") as tar:

            for directory in directories:
                path_to_dir = path.join(home, directory)
                tar.add(path_to_dir, arcname=directory)
    except IOError as e:
        remove(file_path)
        raise e

    return archive_name


def recover(file_path):
    with tarfile.open(file_path, "r:gz") as tar:
        for directory in directories:
            if directory not in tar.getnames():
                raise Exception("Archive is wrong.")

    sh.sudo('/usr/local/bin/screenly_utils.sh', 'recover', path.abspath(file_path))

    remove(file_path)

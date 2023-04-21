import platform
from pathlib import Path
from pygeoweaver.utils import download_geoweaver_jar, get_geoweaver_jar_path, get_home_dir, check_os


#######################  utils.py  #######################
def test_can_download_geoweaver():
    download_geoweaver_jar()
    if not Path(get_geoweaver_jar_path()).is_file():
        raise FileNotFoundError("Geoweaver jar file failed to download")


def test_get_home_dir():
    # return home POSIX path of OS
    assert Path.home() == Path(get_home_dir())


def test_check_os():
    # should always return an int
    assert type(check_os()) == int


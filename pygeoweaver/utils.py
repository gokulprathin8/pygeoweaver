import os
import sys
import shutil
import logging
import subprocess
import requests
import platform

from IPython import get_ipython


def get_home_dir():
    return os.path.expanduser("~")


def get_root_dir():
    head, tail = os.path.split(__file__)
    return head


def get_java_bin_from_which():
    system = platform.system()

    if system == "Darwin" or system == "Linux":

        try:

            java_bin_sh = f"{get_root_dir()}/java_bin.sh"

            os.chmod(java_bin_sh, 0o755)

            output = subprocess.check_output([java_bin_sh], encoding="utf-8")

            java_bin_path = output.strip()

        except subprocess.CalledProcessError as e:

            print(f"Command execution failed: {e.output}")

            return None

    elif system == "Windows":

        print("Unsupported platform for windows yet.")

    else:
        print("Unsupported platform.")

    return java_bin_path

def check_homebrew_installation():
    try:
        subprocess.run(["brew", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def install_homebrew():
    """Install Homebrew."""
    try:
        print("Installing Homebrew...")
        subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                       shell=True, check=True)
        print("Homebrew installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Homebrew: {e}")

def get_java_bin_path():
    java_bin_path = None  # by `None` we assume java is not installed on the user system
    os_name = platform.system().lower()

    # now get java bin path, from the installation
    if os_name == "windows":
        java_bin_path = subprocess.check_output("where java",
                                                stderr=subprocess.STDOUT, shell=True).decode().strip().split('\n')[0]
    if os_name in ["linux", "darwin"]:
        java_bin_path = subprocess.check_output("where java", stderr=subprocess.STDOUT, shell=True).decode().strip()

    if java_bin_path is None:
        # if the `path` is None, it means java is not installed on the user PC.
        if os_name == "linux":
            cmd = "sudo apt update -y && sudo apt install default-jdk -y && java --version"
            subprocess.run(cmd, shell=True, stderr=subprocess.STDOUT)
            java_bin_path = subprocess.check_output("where java", stderr=subprocess.STDOUT, shell=True).decode().strip()
        if os_name == "darwin":
            if check_homebrew_installation():
                print("Homebrew is already installed")
            else:
                install_homebrew()

            cmd = "brew install openjdk@11"
            subprocess.run(cmd, shell=True, stderr=subprocess.STDOUT)
            java_bin_path = subprocess.check_output("where java", stderr=subprocess.STDOUT, shell=True).decode().strip()
        if os_name == "windows":
            pass

    return java_bin_path


def get_module_absolute_path():
    module_path = os.path.abspath(__file__)
    return os.path.dirname(module_path)


def get_geoweaver_jar_path():
    return f"{get_home_dir()}/geoweaver.jar"


def check_geoweaver_jar():
    return os.path.isfile(get_geoweaver_jar_path())


def download_geoweaver_jar(overwrite=False):
    if check_geoweaver_jar():
        if overwrite:
            os.remove(get_geoweaver_jar_path())
        else:
            system = platform.system()
            if not system == "Windows":  # Windows files are exec by default
                subprocess.run(
                    ["chmod", "+x", get_geoweaver_jar_path()], cwd=f"{get_root_dir()}/"
                )
                return

    print("Downloading latest version of Geoweaver...")
    geoweaver_url = (
        "https://github.com/ESIPFed/Geoweaver/releases/download/latest/geoweaver.jar"
    )
    r = requests.get(geoweaver_url)

    with open(get_geoweaver_jar_path(), "wb") as f:
        f.write(r.content)

    if check_geoweaver_jar():
        print("Geoweaver.jar is downloaded")

    else:
        raise RuntimeError("Fail to download geoweaver.jar")


def check_os():
    if platform.system() == "Linux" or platform == "Linux2":
        return 1
    elif platform.system() == "Darwin":
        return 2
    elif platform.system() == "Windows":
        return 3


def check_ipython():
    try:
        return get_ipython().__class__.__name__ == "ZMQInteractiveShell"
    except:
        return False


def get_logger(class_name):
    logger = logging.getLogger(class_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def copy_files(source_folder, destination_folder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_file = os.path.join(root, file)
            destination_file = os.path.join(
                destination_folder, os.path.relpath(source_file, source_folder)
            )
            os.makedirs(os.path.dirname(destination_file), exist_ok=True)
            shutil.copy2(source_file, destination_file)

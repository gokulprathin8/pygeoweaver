
import subprocess
from pygeoweaver.utils import download_geoweaver_jar, get_geoweaver_jar_path, get_root_dir


def reset_password(password):
  """
  Usage: <main class> resetpassword
  Reset password for localhost
  """
  download_geoweaver_jar()
  subprocess.run(f"java -jar {get_geoweaver_jar_path()} resetpassword -p {password}", shell=True)


import subprocess
import urllib.request


def start(self) -> None:
    urllib.request.urlretrieve(self.download_url, filename=self.filename)
    self.process = subprocess.Popen(f'java -jar {self.filename}'.split(),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    stdout, stderr = self.process.communicate()
    print(
        stdout,
        stderr
    )

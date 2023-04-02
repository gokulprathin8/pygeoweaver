from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='pygeoweaver',
    version='0.0.1',
    description="Python binding for Geoweaver",
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    # license='MIT',
    packages=find_packages(),
    author='Ziheng Sun',
    author_email='zsun@gmu.edu',
    keywords=['Geoweaver', 'Workflow'],
    url='https://github.com/ZihengSun/pygeoweaver',
    download_url=''
)

install_requires = [

]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
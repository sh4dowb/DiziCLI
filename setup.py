#!/usr/bin/env python
from setuptools import find_packages,setup

version = '1.0.0'
setup(
    name='dizicli',
    version=version,
    description='Dizi Crawler',
    author='Batuhan Osman Taskaya',
    author_email='batuhanosmantaskaya@gmail.com',
    url='https://github.com/btaskaya/dizicli',
    download_url='https://github.com/btaskaya/dizicli',
    entry_points={
        'console_scripts': [
            'dizicli = dizicli.bin:main',
            'filmcli = dizicli.bin_movie:main'
        ],
    },
    install_requires=['requests', 'pyquery', 'demjson', 'pget', 'furl', 'PyExecJS'],
    packages=find_packages(exclude=("tests", "tests.*")),
)

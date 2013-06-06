import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='crutool',
    version='1.0',
    author='Philipp Kewisch',
    author_email='mozilla@kewis.ch',
    description='Crucible and JIRA manipulation tool',
    license = "MPL2",
    keywords="jira crucible atlassian",
    url='http://github.com/kewisch/crutool/',
    packages=['crutool', 'tests'],
    long_description=read('README.md'),
    scripts=['bin/crutool'],
    install_requires=[
        "keyring >= 1.3",
        "iniparse >= 0.4"
    ],
    data_files=[('', ['data/crutoolrc'])]
)

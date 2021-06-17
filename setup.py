import os

from setuptools import setup, find_namespace_packages

_SCRIPT_DIR = os.path.dirname(__file__)


def read_readme():
    with open(os.path.join(_SCRIPT_DIR, 'README.md'), 'r') as f:
        return f.read()


setup(
    name='seekret.apitest',
    version='0.1.2',
    author='Seekret Software Ltd.',
    author_email='info@seekret.com',
    description="Seekret's library for API testing runtime",
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    packages=find_namespace_packages(include=('seekret.apitest',
                                              'seekret.apitest.*')),
    install_requires=['python-box~=5.3.0', 'requests~=2.25', 'tavern~=1.15.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    project_urls={
        'Bug Tracker': 'https://github.com/seek-ret/tests-rtl/issues'
    },
    url='https://github.com/seek-ret/tests-rtl')

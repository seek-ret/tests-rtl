from setuptools import setup, find_namespace_packages

setup(name='seekret.apitest',
      description="Seekret's library for API testing runtime",
      version='0.1.0',
      package=find_namespace_packages(include=('seekret.apitest', 'seekret.apitest.*')),
      install_requires=['python-box~=5.3.0'])

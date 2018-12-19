from setuptools import setup, find_packages

setup(
    name='bifrostlib',
    version='1.0',
    description='Datahandling functions for bifrost (later to be API interface)',
    url='https://github.com/ssi-dk/bifrost-private/tree/master/lib/bifrostlib',
    author="Kim Ng",
    author_email="kimn@ssi.dk",
    packages=find_packages(),
    install_requires=['ruamel.yaml', 'pymongo']
    )

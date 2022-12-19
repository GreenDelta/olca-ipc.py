from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='olca-ipc',
    version='0.0.12',
    description='A Python package for calling openLCA functions from Python.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/GreenDelta/olca-ipc.py',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=['requests'],
    include_package_data=True,
    keywords=['openLCA', 'life cycle assessment', 'LCA'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities",
    ]
)

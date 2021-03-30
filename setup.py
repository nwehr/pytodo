#
# Copyright (c) Nathan Wehr <nathan@wehrholdings.com>, All rights reserved.
#

from setuptools import setup # type: ignore
from setuptools import find_packages

setup(
   # Application name:
    name="pytodo",

    # Version number (initial):
    version="0.4.0",

    # Application author details:
    author="Nathan Wehr",
    author_email="nathan@wehrholdings.com",

    # Packages
    packages=find_packages(),

    # Include additional files into the package
    include_package_data=True,

    # Details
    # url="http://pypi.python.org/pypi/MyApplication_v010/",

    #
    # license="LICENSE.txt",
    description="Todo app",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
         "pyyaml",
         "requests",
        # "clipboard",
    ],

    entry_points={
        "console_scripts": [
            'pyt = pytodo.main:main'
        ]
    }
)

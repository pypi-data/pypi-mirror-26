# from __future__ import unicode_literals
import os

from setuptools import setup, find_packages
from codecs import open

base_dir = os.path.dirname(__file__)
src_dir = os.path.join(base_dir, "src")


about = {}
with open(os.path.join(src_dir, "oneid", "__about__.py"), encoding='utf-8') as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, "README.rst"), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    long_description=long_description,
    url=about['__uri__'],
    author=about['__author__'],
    author_email=about['__email__'],
    license=about['__license__'],
    classifiers=[
        'Development Status :: 4 - Beta',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        'Topic :: Security :: Cryptography',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='Neustar Trusted Device Identity (TDI) IoT Authentication',
    package_dir={"": "src"},
    packages=find_packages(where='src',
                           exclude=['contrib', 'docs', 'tests*',
                                    'venv', 'example*', '*egg-info',
                                    '.gitignore']),
    package_data={
        'oneid': ['data/*.yaml'],
    },
    install_requires=['cryptography>=2.0.2,<2.1', 'PyYAML>=3.11,<4',
                      'requests[security]>=2.18.4,<2.19', 'python-dateutil>=2.6.1,<2.7',
                      'pytz>=2017.2', 'six>=1.11.0,<1.12', 'boto3>=1.4.4,<1.5'],
)

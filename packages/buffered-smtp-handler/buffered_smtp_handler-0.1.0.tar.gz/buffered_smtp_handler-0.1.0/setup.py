import os
from os.path import abspath, dirname, join
from setuptools import setup

__version__ = None

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Get proper long description for package
current_dir = dirname(abspath(__file__))
description = open(join(current_dir, "README.rst")).read()
changes = open(join(current_dir, "CHANGES.rst")).read()
long_description = '\n\n'.join([description, changes])
exec(open(join(current_dir, "pierky/buffered_smtp_handler/version.py")).read())

install_requires = []

# Get the long description from README.md
setup(
    name="buffered_smtp_handler",
    version=__version__,

    packages=["pierky", "pierky.buffered_smtp_handler"],
    namespace_packages=["pierky"],

    license="GPLv3",
    description="A buffered logging handlers that mimics SMTPHandler",
    long_description=long_description,
    url="https://github.com/pierky/bufferedsmtphandler",
    download_url="https://github.com/pierky/bufferedsmtphandler",

    author="Pier Carlo Chiodi",
    author_email="pierky@pierky.com",
    maintainer="Pier Carlo Chiodi",
    maintainer_email="pierky@pierky.com",

    install_requires=install_requires,

    keywords=['logging', 'python'],

    classifiers=[
        "Development Status :: 4 - Beta",

        "Environment :: Console",

        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Intended Audience :: Developers",

        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Operating System :: POSIX",
        "Operating System :: Unix",

        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",

        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
    ]
)

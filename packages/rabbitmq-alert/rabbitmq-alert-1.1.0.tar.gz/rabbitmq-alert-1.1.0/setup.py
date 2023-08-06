#! /usr/bin/python2

from setuptools import setup, find_packages

# remember to push a new tag after changing this!
VERSION = "1.1.0"

setup(
    name="rabbitmq-alert",
    version=VERSION,
    long_description=open("README.rst").read(),
    packages=find_packages(exclude=["*tests*"]),
    description="Send notifications when predefined conditions are met",
    author="Germano Fronza, Kostas Milonas",
    author_email="germano.inf@gmail.com",
    url="https://github.com/gfronza/rabbitmq-alert",
    download_url="https://github.com/gfronza/rabbitmq-alert/tarball/"+VERSION,
    keywords=["rabbitmq", "alert", "monitor"],
    classifiers=[],
    entry_points={
        "console_scripts": [
            "rabbitmq-alert = rabbitmqalert:rabbitmqalert.main"
        ]
    },
    data_files=[('/etc/rabbitmq-alert/', ['config.ini.example'])]
)

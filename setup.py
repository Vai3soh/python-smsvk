# -*- coding: utf-8 -*-
from os import path
from setuptools import setup

def long_description():
    """Build the description from README file """
    this_dir = path.abspath(path.dirname(__file__))
    with open(path.join(this_dir, 'README.md'), encoding='utf-8') as f:
        return f.read()


def requirements():
    """Build the requirements list for this project"""
    requirements_list = list()
    with open('requirements.txt') as pc_requirements:
        for install in pc_requirements:
            requirements_list.append(install.strip())
    return requirements_list


setup(
    name='smsvk',
    version='1.0',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    description='Wrapper for automatic reception of SMS-messages by smsvk.net',
    author='',
    license='Apache License, Version 2.0, see LICENSE file',
    keywords='sms, revice, smsvk, autoreg',
    author_email='',
    url='',
    download_url='',
    packages=['smsvk'],
    install_requires=requirements(),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)

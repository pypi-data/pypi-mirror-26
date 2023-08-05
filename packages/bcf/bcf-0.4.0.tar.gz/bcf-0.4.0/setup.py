#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = ['appdirs>=1.4', 'argcomplete>=1.8', 'pyserial>=3.0']

setup(
    name='bcf',
    packages=["bcf"],
    package_dir={'': '.'},
    version='0.4.0',
    description='BigClown Firmware Tool.',
    author='Hardwario s.r.o.',
    author_email='karel.blavka@bigclown.com',
    url='https://github.com/bigclownlabs/bch-firmware-tool',
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords=['BigClown', 'bcf', 'firmware', 'flasher'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Environment :: Console'
    ],
    entry_points='''
        [console_scripts]
        bcf=bcf.cli:main
    ''',
    long_description='''
BigClown Firmware Tool.
'''
)

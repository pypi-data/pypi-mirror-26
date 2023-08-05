#!/usr/bin/env python

"""
Installer for KKBOX SDK
"""

from distutils.core import setup

setup(name='kkbox_developer_sdk',
      description='KKBOX Open API Developer SDK for Python',
      author='Sharon Yang',
      author_email='sharonyang@kkbox.com',
      version='1.0.0',
      url='https://github.com/KKBOX/kkbox_openapi_developer_sdk',
      download_url='https://github.com/KKBOX/kkbox_openapi_developer_sdk/tarball/v1.0.0',
      packages=['kkbox_developer_sdk'],
      package_dir={'kkbox_developer_sdk': 'kkbox_developer_sdk'},
      keywords=['KKBOX', 'Open', 'API', 'OpenAPI'])

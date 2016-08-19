#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

config = {
    'setup_requires': ['setuptools-markdown'],
    'name': 'glacier-backup',
    'description': 'Maintain backups locally (with rotation) and with glacier',
    'long_description_markdown_filename': 'README.md',
    'keywords': 'backup glacier aws rotation',
    'author': 'Digital Surgeons',
    'url': 'https://github.com/digitalsurgeons/glacier-backup',
    'version': '0.1.0',
    'packages': ['glacierbackup'],
    'entry_points': {
        'console_scripts': [
            'glacier-backup=cli:main',
        ],
    },
    'install_requires': ['archive-rotator', 'boto3'],
    'extras_require': {
        'test': ['nose'],
    },
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Environment :: Console',
        'Topic :: System :: Archiving :: Backup',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
    ],
}

setup(**config)

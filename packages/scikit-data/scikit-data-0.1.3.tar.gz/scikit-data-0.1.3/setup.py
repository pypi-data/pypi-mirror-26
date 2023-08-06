#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pandas',
    'numpy',
    'scipy',
    'scikit-learn',
    'matplotlib',
    'ipython',
    'jupyter',
    'ipywidgets',
    'h5py',
    'odo'
]

test_requirements = [
    # TODO: put package test requirements here
]

def get_version():
    """Obtain the version number"""
    import imp
    import os
    mod = imp.load_source(
        'version', os.path.join('skdata', '__init__.py')
    )
    return mod.__version__

setup(
    name='scikit-data',
    version=get_version(),
    description="The propose of this library is to allow the data analysis process more easy and automatic.",
    long_description=readme + '\n\n' + history,
    author="Ivan Ogasawara",
    author_email='ivan.ogasawara@gmail.com',
    url='https://github.com/OpenDataScienceLab/skdata',
    download_url = 'https://github.com/OpenDataScienceLab/skdata/archive/master.tar.gz',
    packages=[
        'skdata',
    ],
    package_dir={'skdata':
                 'skdata'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='scikit data analysis',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

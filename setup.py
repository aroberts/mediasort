#!/usr/bin/env python

from setuptools import setup, find_packages
version = "1.0"

long_description = """
Perform an action based on media type
"""

setup(
    name='mediasort',
    version=version,
    description='Media type detection',
    license='BSD',

    long_description=long_description,
    author='Andrew Roberts',
    author_email='adroberts@gmail.com',
    url='https://github.com/aroberts',

    packages=find_packages(),

    install_requires=['requests', 'PyYAML', 'click'],

    entry_points={
        'console_scripts': [
            'mediasort = mediasort.cli:cli',
        ]
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)

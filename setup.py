#!/usr/bin/env python

# Support setuptools only, distutils has a divergent and more annoying API and
# few folks will lack setuptools.
from setuptools import setup, find_packages

# Version info -- read without importing
# _locals = {}
# with open('_version.py') as fp:
#     exec(fp.read(), None, _locals)
#     version = _locals['__version__']
version = "0.1"

# Frankenstein long_description: version-specific changelog note + README
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
            'mediasort = mediasort.cli:classify',
        ]
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
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

#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

# the name of the project
name = 'ipyscales'

#-----------------------------------------------------------------------------
# Minimal Python version sanity check
#-----------------------------------------------------------------------------

import sys

v = sys.version_info
if v[:2] < (2, 7) or (v[0] >= 3 and v[:2] < (3, 3)):
    # Note: 3.3 is untested, but we'll still allow it
    error = "ERROR: %s requires Python version 2.7 or 3.3 or above." % name
    print(error, file=sys.stderr)
    sys.exit(1)

#-----------------------------------------------------------------------------
# get on with it
#-----------------------------------------------------------------------------

import io
import os
from glob import glob

from setuptools import setup, find_packages

from setupbase import (create_cmdclass, install_npm, ensure_targets,
    combine_commands)

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))

# Representative files that should exist after a successful build
jstargets = [
    os.path.join(here, name, 'nbextension', 'static', 'extension.js'),
    os.path.join(here, 'packages', 'jlextension', 'build', 'index.js'),
]

version_ns = {}
with io.open(pjoin(here, name, '_version.py'), encoding="utf8") as f:
    exec(f.read(), {}, version_ns)


cmdclass = create_cmdclass(('jsdeps',))
cmdclass['jsdeps'] = combine_commands(
    install_npm(here),
    ensure_targets(jstargets),
)

package_data = {
    name: [
        'nbextension/static/*.*',
    ]
}


setup_args = dict(
    name            = name,
    description     = 'A widget library for scales',
    version         = version_ns['__version__'],
    scripts         = glob(pjoin('scripts', '*')),
    cmdclass        = cmdclass,
    packages        = find_packages(here),
    package_data    = package_data,
    author          = 'Jupyter Development Team',
    author_email    = 'jupyter@googlegroups.com',
    url             = 'https://github.com/vidartf/ipyscales',
    license         = 'BSD',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Jupyter', 'Widgets', 'IPython'],
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Jupyter',
    ],
)


setuptools_args = {}
install_requires = setuptools_args['install_requires'] = [
    'ipywidgets>=7.0.0',
]

extras_require = setuptools_args['extras_require'] = {
    'test': [
        'pytest',
        'pytest-cov',
        'nbval',
    ],
    'docs': [
        'sphinx',
        'recommonmark',
        'sphinx_rtd_theme'
    ],
}

if 'setuptools' in sys.modules:
    setup_args.update(setuptools_args)

    setup_args.pop('scripts', None)

    setup_args.update(setuptools_args)

if __name__ == '__main__':
    setup(**setup_args)

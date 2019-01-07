#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
from setuptools import setup, find_packages
import io

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip


__version__ = '0.1'


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


pfile = Project(chdir=False).parsed_pipfile
install_requires = convert_deps_to_pip(pfile['packages'], r=False)
tests_require = convert_deps_to_pip(pfile['dev-packages'], r=False)

with open('requirements.txt', 'w+') as f:
    f.writelines('\n'.join(install_requires))
    f.write('\n')
    f.writelines('\n'.join(tests_require))

setup(
    name='bbtest',
    url='aaa',
    author='aaa',
    author_email='aaa',
    version=__version__,
    install_requires=install_requires,
    description='automation framework for black box testing',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    charset='UTF-8',
    variant='GFM',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    tests_require=tests_require,
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.7',
        ])

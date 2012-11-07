#!/usr/bin/env python

from setuptools import setup

setup(
    name='rst2html5',
    version='0.1',
    author='Mariano Guerra',
    author_email='luismarianoguerra@gmail.com',
    url='https://github.com/marianoguerra/rst2html5',
    long_description=open('README.rst').read(),
    packages=['html5css3'],
    scripts = ['bin/rst2html5'],
    include_package_data = True,
    install_requires=['docutils'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
)


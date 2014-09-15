#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup

setup(
    name='rst2html5-tools',
    version='0.2',
    author='Mariano Guerra',
    author_email='luismarianoguerra@gmail.com',
    url='https://github.com/marianoguerra/rst2html5',
    description='Transform restructuredtext documents to html5',
    long_description=open('README.rst').read(),
    packages=['html5css3'],
    package_data={'html5css3': ['thirdparty/*/*.*']},
    include_package_data=True,
    install_requires=['docutils'],
    entry_points={
        'console_scripts': [
            'rst2html5 = html5css3.main:main',
        ]},
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

#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup

setup(
    name='rst2html5-tools',
    version='0.5.1',
    author='Mariano Guerra',
    description="Transform reStructuredText documents to html5 + twitter's bootstrap css, deck.js or reveal.js",
    author_email='luismarianoguerra@gmail.com',
    url='https://github.com/marianoguerra/rst2html5',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities',
    ],
)

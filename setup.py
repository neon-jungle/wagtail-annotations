#!/usr/bin/env python
"""
Install wagtailvideos using setuptools
"""

from setuptools import find_packages, setup
with open('README.rst', 'r') as f:
    readme = f.read()


setup(
    name='wagtail-annotations',
    version='3.0.0',
    description="A wagtail module for creating an image field with annotation metadata",
    long_description=readme,
    author='Neon Jungle',
    author_email='developers@neonjungle.studio',
    url='https://github.com/neon-jungle/wagtailannotatedimage',

    install_requires=[
        'wagtail>=2.7',
        'Django>=2.0',
    ],
    extras_require={
        'testing': [
            'selenium==3.0.0'
        ]
    },
    zip_safe=False,
    license='BSD License',

    packages=find_packages(),

    include_package_data=True,
    package_data={},

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ],
)

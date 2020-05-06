#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'libcst']

setup_requirements = ['pytest-runner']

test_requirements = ['pytest>=3']

setup(
    author="Bruno Alla",
    author_email='alla.brunoo@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Codemod to help upgrading to newer versions of Django",
    entry_points={
        'console_scripts': [
            'django_codemod=django_codemod.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='django,codemod',
    name='django-codemod',
    packages=find_packages(include=['django_codemod', 'django_codemod.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/browniebroke/django-codemod',
    version='0.1.0',
    zip_safe=False,
)

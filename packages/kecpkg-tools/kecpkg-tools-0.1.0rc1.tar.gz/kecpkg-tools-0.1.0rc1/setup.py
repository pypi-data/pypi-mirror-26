from glob import glob
from io import open

import os
from setuptools import find_packages, setup

with open('kecpkg/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

if os.path.exists('pyproject.toml'):
    import toml
    pyproject = toml.load('pyproject.toml')

    REQUIRES = pyproject.get('requires') and  pyproject.get('requires').get('requires') or []
    TEST_REQUIRES = pyproject.get('requires') and pyproject.get('requires').get('testing_requires') or []
else:
    REQUIRES = ['']
    TEST_REQUIRES = ['coverage', 'pytest']

setup(
    name='kecpkg-tools',
    version=version,
    description='',
    long_description=readme,
    author='Jochem Berends',
    author_email='jochem.berends@ke-works.com',
    maintainer='Jochem Berends',
    maintainer_email='jochem.berends@ke-works.com',
    url='https://github.com/_/kecpkg-tools',
    license='Apache-2.0',

    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    install_requires=REQUIRES,
    tests_require=TEST_REQUIRES,

    packages=find_packages(exclude=['tests']),

    package_data={
        'kecpkg': ['files/templates/*.template'],
                   # 'files/templates/readme.md.template',
                   # 'files/templates/requirements.txt.template',
                   # 'files/templates/script.py.template'],
    },

    entry_points={
        'console_scripts': (
            'kecpkg = kecpkg.cli:kecpkg',
        ),
    }
)

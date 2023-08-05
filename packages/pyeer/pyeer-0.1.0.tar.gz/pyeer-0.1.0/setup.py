# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

# Get the long description from the README file
with open('README.rst') as f:
    readme = f.read()

setup(
    # Package name
    name='pyeer',

    # Package version
    version='0.1.0',

    entry_points={
        'console_scripts': [
            'geteerinf = pyeer.eer_info:get_eer_info',
        ],
    },

    include_package_data=True,

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        'pyeer': ['example_files/hist/*.txt', 'example_files/non_hist/*.txt'],
    },

    # Included packages
    packages=find_packages(),

    # Package author information
    author=u'Manuel Aguado Martínez',
    author_email='manuelaguadomtz@gmail.com',
    url='https://www.researchgate.net/profile/Manuel_Aguado_Martinez2',

    # Package requirements
    install_requires=['numpy',
                      'matplotlib'],

    # Package description
    description='A python package with utilities to calculate Equal Error Values,'
                ' operation points and to plot the probability error curves.',
    long_description=readme,
    keywords=['Equal Error Rate', 'False Matching Rate', 'False Non-matching rate', 'ROC', 'DET', 'EER', 'FMR', 'FNMR'],

)
from setuptools import setup

install_requires = [
    'httplib2',
    'ujson',
    'jsonschema', # only needed for a test
    'jmespath', # optional, can work without it
    'pandas == 0.20.1', # optional, can work without it
    'ase == 3.11' # can be pymatgen instead
]

setup(
    name='mpds_client',
    version='0.0.8',
    author='Evgeny Blokhin',
    author_email='eb@tilde.pro',
    description='MPDS platform API client',
    long_description='This Python library takes care of many aspects of the [MPDS platform API](http://developer.mpds.io), such as pagination, error handling, validation, proper data extraction and more. We encourage our users to adopt this library for their needs.',
    url='https://github.com/mpds-io/python-api-client',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='materials informatics crystal structures phase diagrams physical properties PAULING FILE MPDS platform API',
    packages=['mpds_client'],
    install_requires=install_requires
)

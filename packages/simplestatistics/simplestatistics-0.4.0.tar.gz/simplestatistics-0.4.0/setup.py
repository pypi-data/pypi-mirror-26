"""
setup.py for simplestatistics package
"""
from distutils.core import setup

setup(
    name='simplestatistics',
    packages=['simplestatistics', 'simplestatistics.statistics'],
    version='0.4.0',
    description='Simple statistical functions implemented in readable Python.',
    author='Sherif Soliman',
    author_email='sherif@ssoliman.com',
    license='MIT',
    url='https://github.com/sheriferson/simplestatistics',
    download_url='https://github.com/sheriferson/simplestatistics/tarball/0.4.0',
    keywords=['statistics', 'math'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Topic :: Education',
        'Topic :: Utilities'
        ]
)

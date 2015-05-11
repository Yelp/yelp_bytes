from setuptools import setup

setup(
    name='yelp_bytes',
    description='Utilities for dealing with byte strings, invented and maintained by Yelp.',
    url='https://github.com/Yelp/yelp_bytes',
    version='0.2.0',

    author='Buck Evan',
    author_email='buck@yelp.com',

    platforms='all',
    classifiers=[
        'License :: Public Domain',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    install_requires=['yelp_encodings'],

    py_modules=['yelp_bytes'],
)

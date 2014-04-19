from setuptools import setup

setup(
    name='yelp_bytes',
    description='Utilities for dealing with byte strings, invented and maintained by Yelp.',
    url='https://github.com/Yelp/yelp_bytes',
    version='0.1.1',

    author='Buck Golemon',
    author_email='buck@yelp.com',

    platforms='all',
    classifiers=[
        'License :: Public Domain',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=['yelp_encodings'],

    py_modules=['yelp_bytes'],
)

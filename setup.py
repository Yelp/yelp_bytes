from setuptools import find_packages
from setuptools import setup

setup(
    name='yelp_bytes',
    description='Utilities for dealing with byte strings, invented and maintained by Yelp.',
    url='https://github.com/Yelp/yelp_bytes',
    version='0.4.4',

    author='Buck Evan',
    author_email='buck@yelp.com',

    platforms='all',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: The Unlicense (Unlicense)',
    ],
    python_requires='>=3.6',
    package_data={
        'yelp_bytes': ['py.typed'],
    },
    install_requires=['yelp_encodings'],
    packages=find_packages(exclude=["tests*"]),
)

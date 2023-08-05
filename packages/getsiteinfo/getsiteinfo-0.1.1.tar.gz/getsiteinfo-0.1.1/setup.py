from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='getsiteinfo',
    version='0.1.1',
    description='Get site information',
    long_description=long_description,
    url='https://github.com/kaywang26/getsiteinfo',
    author='Kay Wang',
    author_email='kay.wang26@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['bs4', 'selenium'],
    packages=['getsiteinfo'],
)
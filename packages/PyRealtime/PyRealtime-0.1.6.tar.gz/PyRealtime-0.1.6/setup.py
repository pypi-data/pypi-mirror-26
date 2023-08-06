from setuptools import setup, find_packages

setup(
    name="PyRealtime",
    version="0.1.6",
    packages=find_packages(),
    description='A package for realtime data processing, including reading from serial ports and plotting.',
    author='Eric Whitmire',
    author_email='emwhit@cs.washington.edu',
    url='https://github.com/ewhitmire/pyrealtime',
    keywords=['realtime', 'plotting', 'serialport', 'logging', 'pipeline']
)
import os
from setuptools import setup, find_packages
from pathlib import Path

NAME = "pypony"
VERSION = os.environ['PYPONY_RELEASE_VERSION']

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open("requirements.txt", "r") as fp:
    requirements = fp.readlines()

setup(
    name=NAME,
    version=VERSION,
    description='A python utility for contract testing APIs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Bandwidth',
    author_email='letstalk@bandwidth.com',
    url='https://github.com/Bandwidth/pypony/',
    py_modules=['pypony', 'src'],
    install_requires=requirements,
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        pypony=pypony:cli
    """,
)

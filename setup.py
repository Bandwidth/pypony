from setuptools import setup

with open("requirements.txt", "r") as fp:
    requirements = fp.readlines()

setup(
    name='PyPony',
    description='A python utility for contract testing APIs',
    author='Bandwidth',
    author_email='letstalk@bandwidth.com',
    url='https://github.com/Bandwidth/pypony/',
    version='0.1.0',
    py_modules=['pypony'],
    install_requires=requirements,
)

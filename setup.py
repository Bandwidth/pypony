from setuptools import setup

with open("requirements.txt", "r") as fp:
    requirements = fp.readlines()

setup(
    name='PyApi',
    description='A python utility for contract testing APIs',
    author='Bandwidth',
    author_email='letstalk@bandwidth.com',
    url='https://github.com/Bandwidth/pyapi/',
    version='0.1.0',
    py_modules=['pyapi'],
    install_requires=requirements,
)

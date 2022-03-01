from setuptools import setup, find_packages

with open("requirements.txt", "r") as fp:
    requirements = fp.readlines()

setup(
    name='PyPony',
    description='A python utility for contract testing APIs',
    author='Bandwidth',
    author_email='letstalk@bandwidth.com',
    url='https://github.com/Bandwidth/pypony/',
    version='0.1.0',
    py_modules=['pypony', 'src'],
    install_requires=requirements,
    packages = find_packages(exclude=["website", "test"]),
    entry_points = '''
        [console_scripts]
        pypony=pypony:cli
    '''
)

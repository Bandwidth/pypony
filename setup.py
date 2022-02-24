from setuptools import setup

with open("requirements.txt", "r") as fp:
    requirements = fp.readlines()

setup(
    name="API Validator",
    version="0.4.0",
    py_modules=["api_validator"],
    install_requires=requirements,
)

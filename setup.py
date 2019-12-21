from setuptools import setup, find_packages
from os import path

pwd = path.abspath(path.dirname(__file__))

with open(path.join(pwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

pkgs_requires = [
    'flask==1.1.1',
    'flask_restful==0.3.7',
    'PyJWT==1.7.1'
]

setup(
    name='luizalabs_project',
    version='0.0.1',
    long_description=long_description,
    author='Gabriel de Melo Vaz Nogueira',
    install_requires=pkgs_requires
)
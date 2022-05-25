from setuptools import setup
from os import path

pwd = path.abspath(path.dirname(__file__))

with open(path.join(pwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

pkgs_requires = [
    'flask==1.1.1',
    'flask_restful==0.3.7',
    'flasgger==0.9.3',
    'PyJWT==2.4.0',
    'pymongo==3.10.0',
    'requests==2.22.0',
    'loguru==0.3.2',
    'gunicorn==20.0.4',
    'mockupdb==1.7.0',
    'jsonschema==2.6.0'
]

setup(
    name='luizalabs_project',
    version='0.0.1',
    long_description=long_description,
    author='Gabriel de Melo Vaz Nogueira',
    install_requires=pkgs_requires
)

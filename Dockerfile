FROM python:3.7.6-stretch

EXPOSE 8000

ADD luizalabs_project /luizalabs_project
ADD README.md /luizalabs_project
ADD setup.py /luizalabs_project
WORKDIR /luizalabs_project

RUN python setup.py install


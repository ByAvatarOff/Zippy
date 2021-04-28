FROM python:3.6-alpine

RUN mkdir /dockerSametinder
WORKDIR /dockerSametinder

ADD req.txt /dockerSametinder/


RUN pip install --upgrade pip
RUN pip install -r req.txt

ADD . /dockerSametinder/

FROM python:3.10.5-slim

WORKDIR /balance_list
COPY . /balance_list

RUN pip install -r requirements/base.txt
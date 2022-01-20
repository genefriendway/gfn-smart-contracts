FROM python:3.7.12

# Setting PYTHONUNBUFFERED to a non empty value ensures that the python output
# is sent straight to terminal without being first buffered
ENV PYTHONUNBUFFERED=1

WORKDIR /gfn-smart-contracts

COPY requirements.txt /gfn-smart-contracts/requirements.txt

RUN apt-get update \
    && apt-get install npm -y \
    && npm install -g ganache-cli \
    && pip install -r requirements.txt \
    && brownie pm install OpenZeppelin/openzeppelin-contracts@4.4.1

ADD . /gfn-smart-contracts/

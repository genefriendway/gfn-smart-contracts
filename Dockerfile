FROM python:3.7.12

# Setting PYTHONUNBUFFERED to a non empty value ensures that the python output
# is sent straight to terminal without being first buffered
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt update \
    && apt install gcc g++ make \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt install -y nodejs \
    && npm install -g ganache-cli

ADD requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt \
    && brownie pm install OpenZeppelin/openzeppelin-contracts@4.4.1

ADD package.json /code/package.json

RUN npm install

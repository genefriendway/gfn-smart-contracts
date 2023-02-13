FROM python:3.7.12

# Setting PYTHONUNBUFFERED to a non empty value ensures that the python output
# is sent straight to terminal without being first buffered
ENV PYTHONUNBUFFERED=1

WORKDIR /gfn-smart-contracts

RUN apt update \
    && apt install gcc g++ make \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt install -y nodejs

ADD . /gfn-smart-contracts/

RUN pip install -r requirements.txt \
    && brownie pm install OpenZeppelin/openzeppelin-contracts@4.4.1

RUN npm install

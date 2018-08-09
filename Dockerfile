FROM python:2

ADD ./sources.list /etc/apt/sources.list

RUN apt-get -y update
RUN apt-get -y install git \
				libssl-dev \
				libffi-dev \
				build-essential

RUN pip install --upgrade pip
RUN pip install requests prettytable pwntools pycrypto zio

RUN pip install prompt_toolkit click fuzzyfinder pygments

RUN pip install flask

VOLUME /framelog
VOLUME /app
WORKDIR /app
CMD ["/bin/bash"]

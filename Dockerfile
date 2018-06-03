FROM python:2

RUN apt-get -y update
RUN apt-get -y install git \
				libssl-dev \
				libffi-dev \
				build-essential

RUN pip install --upgrade pip
RUN pip install flask requests prettytable pwntools

VOLUME /app
WORKDIR /app
CMD ["/bin/bash"]

FROM python:2

RUN pip install flask requests IPy

VOLUME /app
WORKDIR /app
CMD ["/bin/bash"]

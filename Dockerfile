FROM python:2.7
ENV PYTHONUNBUFFERED 1

# build arguments
ARG LUCIDA_HOSTNAME
ENV LUCIDA_HOSTNAME $LUCIDA_HOSTNAME

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

FROM python:3.7
MAINTAINER "Salem Hassan <salem4dev@gmail.com>"
COPY ./requirements.txt /requirements.txt
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN pip3 install -r /requirements.txt
RUN mkdir /tweetApp
WORKDIR /tweetApp
ADD ./requirements.txt /tweetApp/requirements.txt
COPY . /tweetApp
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

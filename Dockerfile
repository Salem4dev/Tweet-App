FROM python:3.7
MAINTAINER "Salem Hassan"
COPY ./requirements.txt /requirements.txt
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN pip3 install -r /requirements.txt
RUN mkdir /app
WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
COPY . /app
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
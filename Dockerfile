FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ENV PYTHONPATH /code:$PYTHONPATH
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN python manage.py migrate

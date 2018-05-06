FROM python:3
ADD . /politiprocess
WORKDIR /politiprocess
RUN pip install -r requirements.txt
FROM python:3
ADD . /Politiprocess
WORKDIR /Politiprocess
RUN pip install -r requirements.txt

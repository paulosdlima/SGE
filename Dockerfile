FROM python:3.9

RUN mkdir /home/sge
WORKDIR /home/sge

COPY ./requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5000
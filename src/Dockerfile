FROM ubuntu:latest
RUN apt-get -y update && apt-get install python3 -y && apt-get install python3-pip -y

COPY alert_system.py /usr/src/alert_system.py
COPY consumer.py /usr/src/consumer.py
COPY requirements.txt /usr/src/requirements.txt
COPY lda_model.jl /usr/src/lda_model.jl

WORKDIR /usr/src
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "consumer.py" ]
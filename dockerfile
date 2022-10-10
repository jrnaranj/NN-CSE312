FROM python:3.10

ENV HOME /root
WORKDIR /root
RUN apt-get update --fix-missing
RUN apt-get install -y nodejs
RUN apt-get install -y npm

COPY . .

RUN npm install
RUN pip3 install -r requirements-py.txt

EXPOSE 7878

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && python3 -u app.py
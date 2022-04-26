FROM python:3.8.12-buster

RUN apt-get update \
  && apt install -q -y python3-setuptools \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /build

RUN git clone --depth 1 https://github.com/olpa/zmifanva/
RUN cd /build/zmifanva/web && python3 setup.py install

CMD ["/usr/local/bin/pserve", "/build/zmifanva/web/production.ini"]
EXPOSE 6543

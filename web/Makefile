all:

build-docker: Dockerfile
	docker build -t olpa/zmifanva .

push:
	docker push olpa/zmifanva

# --

host_ip=$(shell ip -o addr show up primary scope global | grep '/24' | head -1 | sed 's@^.*inet @@' | cut -f 1 -d /)

networking=-p 6543:6543 \
  -e MOSES_SERVER_JB2EN=http://$(host_ip):8078 \
  -e MOSES_SERVER_EN2JB=http://$(host_ip):8079

run-dev:
	docker run -it --rm \
	  -v $(shell pwd)/..:/build/zmifanva \
	  $(networking) \
	  olpa/zmifanva \
	  /bin/bash

run-zf-web:
	docker run $(networking) olpa/zmifanva

run-jb-en:
	docker run -it --rm -p 8078:8080 \
	  olpa/moses-zf-jb-en \
	  /opt/moses/bin/moses --server --server-port 8080 \
	    -f /zmifanva/moses_model/jb-en/moses.ini

run-en-jb:
	docker run -it --rm -p 8079:8080 \
	  olpa/moses-zf-en-jb \
	  /opt/moses/bin/moses --server --server-port 8080 \
	    -f /zmifanva/moses_model/en-jb/moses.ini


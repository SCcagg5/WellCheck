FROM node:latest AS FRONT_END

LABEL maintainer="Courtel Eliot"
LABEL maintainermail="eliot.courtel@wanadoo.fr"

WORKDIR /home/front
RUN npm install -g http-server
RUN apt-get install git -y

ENTRYPOINT \
	   if [ -z "$PROD" ] || [ "$PROD" -eq 1 ];then mkdir -p prod; cd prod; cd prod; if [ -d "./WellCheck/" ]; then rm -rf ./WellCheck; fi; git clone --quiet https://github.com/SCcagg5/WellCheck > /dev/null; fi && \
	   if [ -d "./WellCheck/" ]; then cd ./WellCheck/front-end/src && set -a && . ../CONFIG  && http-server -c31536000 ./; fi; \
		 /bin/bash

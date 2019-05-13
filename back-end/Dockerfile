FROM python:3.7  AS BACK_DFC

LABEL maintainer="Courtel Eliot"
LABEL maintainermail="eliot.courtel@wanadoo.fr"

WORKDIR /home/api

ENTRYPOINT \
	   if [ ! -z "$PROD" ] && [ "$PROD" -eq 1 ];then mkdir -p prod; cd prod; if [ -d "./WellCheck/" ]; then rm -rf ./WellCheck; fi; git clone --quiet https://github.com/SCcagg5/WellCheck > /dev/null; fi && \
	   if [ -d "./WellCheck/" ]; then cd ./WellCheck/back-end/src && pip3 install -r ../requirements.txt && python3 server.py > /dev/null; fi;\
	   /bin/bash

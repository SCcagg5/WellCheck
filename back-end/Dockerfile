FROM python:3.7  AS BACK_DFC

LABEL maintainer="Courtel Eliot"
LABEL maintainermail="eliot.courtel@wanadoo.fr"

WORKDIR /home/api

ENTRYPOINT \
	   if [ ! -z "$PROD" ] && [ "$PROD" -eq 1 ];then mkdir prod; cd prod; git clone --quiet https://github.com/SCcagg5/WellCheck > /dev/null; fi && \
	   if [ -d "$DIRECTORY" ]; then cd ./WellCheck/back-end/src && pip3 install -r ../requirements.txt && python3 server.py > /dev/null; fi;\
	   /bin/bash

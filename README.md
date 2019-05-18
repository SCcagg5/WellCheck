# WellCheck

[![CodeFactor](https://www.codefactor.io/repository/github/sccagg5/wellcheck/badge)](https://www.codefactor.io/repository/github/sccagg5/wellcheck)
[![codebeat badge](https://codebeat.co/badges/510f65fa-c690-475b-a1a4-15d214d4750f)](https://codebeat.co/projects/github-com-sccagg5-wellcheck-master)

### Launch the app: 

```bash
 git clone https://github.com/SCcagg5/WellCheck/;   	`# clone the repo`
 cd WellCheck;  					`# enter in the localdir`
 SIG_L='$YOUR_SIGFOX_LOGIN';  				`# setup your login from backend.sigfox`
 SIG_P='$YOUR_SIGFOX_PASSWORD';	 			`# setup your paswd from backend.sigfox`
 echo -e "SIGFOX_LOG='$SIG_L'\nSIGFOX_PASS='$SIG_P'"  	`# echo the proper env var`
 >> back-end/CONFIG;  					`# adding to the configfile`
 docker-compose up -d --build; 			`# launching the docker-compose`
```


# WellCheck

[![CodeFactor](https://www.codefactor.io/repository/github/sccagg5/wellcheck/badge)](https://www.codefactor.io/repository/github/sccagg5/wellcheck)
[![codebeat badge](https://codebeat.co/badges/510f65fa-c690-475b-a1a4-15d214d4750f)](https://codebeat.co/projects/github-com-sccagg5-wellcheck-master)

### Launch the app: 

```bash
 git clone https://github.com/SCcagg5/WellCheck/; 		  	`# clone the repo`
 cd WellCheck;  							`# enter in the localdir`
 SIG_L='$YOUR_SIGFOX_LOGIN';  						`# your login from backend.sigfox`
 SIG_P='$YOUR_SIGFOX_PASSWORD';	 					`# your paswd from backend.sigfox`
 echo -e "SIGFOX_LOG='$SIG_L'\nSIGFOX_PASS='$SIG_P'" >> back-end/CONFIG;`# adding the proper env var`
 docker-compose up -d --build; 						`# launching the docker-compose`
```
### `Dockerfile` comportement:

the api's `dockerfile` is based on python3.7, at launch it:
 * runs in PRODMOD if `$PROD` is ***not set*** or equals ***1***
 * installs needed packages from `back-end/requirements.txt` using `pip3`
 * loads ENV from `back-end/CONFIG`

### PRODMOD: 

The prod mod ignore the shared volume and `git clone` an actual version of the back-end/src/
 
### ENV:

The setup is based on `back-end/CONFIG` it let you define:
```bash
API_HOST='0.0.0.0'				`# INSIDE CONTAINER api host`
API_PORT=8080					`# INSIDE CONTAINER port of the app`
API_SECRET="1q2W3e4R"				`# secret to define token AND PASSWORD`
API_WEBA='*'					`# cors request`
SIGFOX_LOG='5cdd8699e833d974667621XX'		`# `
SIGFOX_PASS='c2bbc9c4cb414df59caecf3964d3b6XX'	`# `
DB_HOST='dbMysql'				`# the host of the mysql database`
DB_USER='root'					`# the user`
DB_PASS='1q2W3e'				`# the password of the user`
DB_NAME='wellcheck' 				`# the database name`
``` 
if the `DB_NAME` is changed you must change it also into `db/mysql-dump/mydb.sql` and `docker-compose`
if the `API_PORT` is change you must change it also into `docker-compose`
`API_WEBA='*'` is not recommended on PRODMOD


----------


### Routes's Basics:

Routes | Methods | Params | Return |
-|-|-|-|
`/register/` | POST | mail, password, password2 | login, mail, token |
`/connect/` | POST | mail, password | login, mail, token |
`/getall/` | POST | mail, token | my_points, shared_to_me |
`/infos/` | POST | mail, token, point_id | id, location, name, surname, data, (shareto or sharefrom) |
`/addpoint/` | POST | mail, token, key, sig_id | id, location, name, surname, data, shareto |
`/surname/` | POST | mail, token, surname | id, location, name, surname, data, (shareto or sharefrom) |
`/share/` | POST | mail, token, mail_to, point_id | id, location, name, surname, data, shareto |

### Routes's Rules:

Routes | Rules |
-|-|
`/register/` | user with the same mail must not exist, <br>passwords must be equals |
`/connect/` | user must exist, <br>creds(`mail` and `password`) must be right |
`/getall/` | user must exist, <br>creds(`mail` and `token`) must be right |
`/infos/` | user must exist, <br>creds(`mail` and `token`) must be right, <br>you must possess or have a share on `point_id` |
`/add_point/`| user must exist, <br>creds(`mail` and `token`) must be right, <br>`sig_id` should be accessible from your backend,sigfox |
`/surname/` | user must exist, <br>creds(`mail` and `token`) must be right, <br>if `surname` equals `""` it will be set to the original `name` of the device |
`/share/` | user must exist, <br>creds(`mail` and `token`) must be right, <br>you must possess `point_id`, <br>`mail_to` must be the mail of an eisting user, <br>`mail_to` must not be your own mail, <br>`mail_to` must not be in your `shareto` list |

### Routes's JSON exemples:

Routes | Body |
-|-|
`/register/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br> "password": "mypasswd",<br> "password2": "mypasswd"<br>} |
`/connect/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br> "password": "mypasswd"<br>} |
`/getall/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br>"token": `YOUR_TOKEN`<br>} |
`/infos/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br>"token": `YOUR_TOKEN`,<br>"point_id" : 1<br>} |
`/addpoint/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br>"token": `YOUR_TOKEN`, <br>"key": `YOUR_DEVICE_KEY`, <br>"sig_id": `YOUR_DEVICE_ID`<br>} |
`/surname/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br>"token": `YOUR_TOKEN`,<br>"surname": "mynewname"<br>} |
`/share/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br>"token": `YOUR_TOKEN`,<br>"mail_to": "anotheruser",<br>"point_id": 1<br>} |

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

### Routes:

Routes | Methods | Params | Return |
-|-|-|-|
`/register/` | POST | mail, password, password2 | login, mail, token |
`/connect/` | POST | mail, password | login, mail, token |
`/getall/` | POST | mail, token | my_points, shared_to_me |
`/infos/` | POST | mail, token, point_id | id, location, name, surname, data, (shareto or sharefrom) |
`/addpoint/` | POST | mail, token, key, sig_id | id, location, name, surname, data, shareto |
`/surname/` | POST | mail, token, surname | id, location, name, surname, data, (shareto or sharefrom) |
`/share/` | POST | mail, token, mail_to, point_id | id, location, name, surname, data, shareto |
``

Routes | Rules |
-|-|
`/register/` | user with the same mail must not exist, <br>passwords must be equals |
`/connect/` | user must exist, <br>creds(`mail` and `password`) must be right |
`/getall/` | user must exist, <br>creds(`mail` and `token`) must be right |
`/infos/` | user must exist, <br>creds(`mail` and `token`) must be right, <br>you must possess or have a share on `point_id` |
`/add_point/`| user must exist, <br>creds(`mail` and `token`) must be right, <br>`sig_id` should be accessible from your backend,sigfox |
`/surname/` | user must exist, <br>creds(`mail` and `token`) must be right, <br>if `surname` equals `""` it will be set to the original `name` of the device |
`/share/` | user must exist, <br>creds(`mail` and `token`) must be right, <br>you must possess `point_id`, <br>`mail_to` must be the mail of an eisting user, <br>`mail_to` must not be your own mail, <br>`mail_to` must not be in your `shareto` list |

Routes | Body |
-|-|
`/register/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br> "password": "mypasswd",<br> "password2": "mypasswd"<br>} |
`/connect/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br> "password": "mypasswd"<br>} |
`/getall/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br>"token": `YOUR_TOKEN`<br>} |
`/infos/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br>"token": `YOUR_TOKEN`,<br>"point_id" : 1<br>} |
`/addpoint/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br>"token": `YOUR_TOKEN`, <br>"key": `YOUR_DEVICE_KEY`, <br>"sig_id": `YOUR_DEVICE_ID`<br>} |
`/surname/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br>"token": `YOUR_TOKEN`,<br>"surname": "mynewname"<br>} |
`/share/` | {<br>"mail": "eliot.courtel@wanadoo.fr",<br>"token": `YOUR_TOKEN`,<br>"mail_to": "anotheruser",<br>"point_id": 1<br>} |

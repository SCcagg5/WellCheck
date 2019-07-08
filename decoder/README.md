# Decoder

Ce microservice consiste à exposer une route appelée par la callback Sigfox, pour acquérir les trames du transmetteur puis les interpréter pour en obtenir les informations

## app.py

Cette API reçoit les trame en en provenance du back-end Sigfox, les déchiffre puis stock toutes les informations présentes dans un fichier de log `activity.log`

### POST /decode

Reçoit la trame en provenance du back-end Sigfox et stock toutes les informations obtenues dans `activity.log`

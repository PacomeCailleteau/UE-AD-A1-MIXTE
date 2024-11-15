# UE-AD-A1-MIXTE


## Base de données MongoDB
Suivre la [documentation](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)
d'installation de MongoDB en local sur Ubuntu. (Faire les 4 premiers points)

Lancer la bd
Ce mettre à la racine du projet puis lancer les commandes suivantes :
```
mkdir -p ./data/db/ 
sudo mongod --dbpath ./data/db/
```
 !!! GARDER LE TERMINAL OUVERT !!!

Se connecter à la bd
`mongosh`

Depuis mongosh, lancer la commande suivante : 
```use tpmixte```

Lancer le script d'import des données du json dans la bd en exécutant le fichier ``init_db.py`` à la racine du projet.

## Lancement du front
Ouvrir un terminal à la racine du projet puis lancer les commandes suivantes :
```
cd  frontend
npm install
npm start
```
Un nouvel onglet s'ouvrira dans votre navigateur par défaut.
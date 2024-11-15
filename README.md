# UE-AD-A1-MIXTE


## Base de données MongoDB
Suivre la [documentation](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/) d'installation de MongoDB en local sur Ubuntu. (Faire les 4 premiers points)

### Création de la base de données mongo local
Ce mettre à la racine du projet puis lancer les commandes suivantes :
```
mkdir -p ./data/db/ 
sudo mongod --dbpath ./data/db/
```
 **GARDER LE TERMINAL OUVERT**

Se connecter à la bd depuis un autre terminal avec la commande suivante :  
`mongosh`

Depuis mongosh, lancer la commande suivante :   
```use tpmixte```

Lancer le script d'import des données du json dans la bd à la racine du projet :   
``pyton3 init_db.py``


## Lancement du front
Ouvrir un terminal à la racine du projet puis lancer les commandes suivantes :
```
cd  frontend
npm install
npm start
```
Un nouvel onglet s'ouvrira dans votre navigateur par défaut.
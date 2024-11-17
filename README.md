# UE-AD-A1-MIXTE
Notre projet offre les microservices suivants :
- showtime sur ce [lien](http://localhost:3002)
- booking sur ce [lien](http://localhost:3003)
- movie sur ce [lien](http://localhost:3001)
- user sur ce [lien](http://localhost:3004)

## Base de données MongoDB
### Installation de MongoDB
Suivre la [documentation](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/) d'installation de MongoDB en local sur Ubuntu. (Faire les 4 premiers points)

### Création de la base de données mongo local
Se mettre à la racine du projet puis lancer les commandes suivantes :
```
mkdir -p ./mongodb
sudo mongod --dbpath ./mongodb
```
 **GARDER LE TERMINAL OUVERT**

Se connecter à la bd depuis un autre terminal avec la commande suivante :  
`mongosh`

Depuis mongosh, lancer la commande suivante :   
```use tpmixte```  
Vous pouvez fermer mongosh.

Lancer le script d'import des données du json dans la bd à la racine du projet :   
``pyton3 init_db.py``  

## Lancer les microservices (à faire après avoir créé la base de données)
Avant de lancer le script run.sh, il faut s'assurer que la base de données est bien lancée.
Le script run.sh permet de lancer la base de données et les microservices en même temps. Pour le lancer, il suffit de taper la commande suivante :  
`./run.sh`

## Lancement du front
Ouvrir un terminal à la racine du projet puis lancer les commandes suivantes :
```
cd  frontend
npm install
npm start
```
Un nouvel onglet s'ouvrira dans votre navigateur par défaut.
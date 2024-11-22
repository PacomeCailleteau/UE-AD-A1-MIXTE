# UE-AD-A1-MIXTE

### Auteurs
- Nicolas CHUSSEAU
- Pacôme CAILLETEAU
- Marina CARBONE
---

## Explication du projet
Ce projet mixte offre les microservices showtime et booking en gRPC, le microservice movie en GraphQL et le microservice user en REST.  
Le microservice user offre les mêmes fonctionnalités que celui présent dans le TP REST.  
Pour la partie bonus, nous avons choisi de rajouter une base de données mongodb en local et de faire un frontend en React.  

### Notre projet offre les microservices suivants :
- Showtime sur ce [lien](http://localhost:3002).
- Booking sur ce [lien](http://localhost:3003).
- Movie sur ce [lien](http://localhost:3001).
- User sur ce [lien](http://localhost:3004).
- Application React sur ce [lien](http://localhost:3000).

## Base de données MongoDB
### Installation de MongoDB
Suivre la [documentation](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/) d'installation de MongoDB en local.

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

## Lancement du front
Ouvrir un terminal à la racine du projet puis lancer les commandes suivantes :
```
cd  frontend
npm install
npm start
```
Un nouvel onglet s'ouvrira dans votre navigateur par défaut.

## Lancer les microservices et le front
Avant de lancer le script run.sh, il faut :
- Installer les dépendances des microservices depuis le fichier requirements.txt.
- Installer les dépendances du front en suivant les instructions ci-dessus.
- Lancer la base de données mongo en suivant les instructions ci-dessus.  

Le script run.sh permet de lancer le front et les microservices en même temps. Pour le lancer, il suffit de taper la commande suivante :  
`./run.sh`  
Si vous rencontrez l'erreur ``$'\r': command not found``, c'est que le fichier run.sh n'est pas en mode unix. Pour le mettre en mode unix, il suffit de taper la commande suivante :
`dos2unix run.sh`

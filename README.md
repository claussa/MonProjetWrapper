# Mon Projet Wrapper

Le but de ce projet est de wrapper mon projet et d'écrire un fichier excel permettant d'avoir une vision d'ensemble des différents camps d'un territoire.

⚠️ Cet outil va lire tous les camps dans l'onglet "Les camps de ma structure" de MonProjet, si vous êtes en soutien d'un camp, celui-ci n'apparaît plus dans cette onglet.
Il faut alors ne plus être en soutien de ce camp, pour que celui-ci soit lu par l'outil.

⚠️ Le fichier de sortie peut-être incomplet, il y a souvent des temps de réponse du serveur qui sont trop long. Vous aurez alors une erreur en éxécutant le script.

## Requirement

Cet outil nécessite Python 3.6.
Ensuite installer les dépendances avec:
```
pip install -r requirements.txt
```

## Utilisation

- Rendez-vous sur MonProjet et identifiez-vous normalement
- Récupérer le token d'authentification généré par l'outil (disponible dans l'onglet Network des outils développeur sur votre navigateur)
- Copier le fichier de config:
```
cp config.yaml.dist config.yaml
```
- Renseigner votre token entre guillemet sur le champs token
- Renseigner les différents codes de groupe de votre territoire moins les 2 derniers chiffres (cela permet de savoir en prenant une unité, dans quel groupe se trouve cette unité).
  Vous pouvez associer un nom à groupe, ces noms seront utilisés sur les différentes feuilles générées dans le fichier excel.
- Enfin vous pouvez lancer la commande suivante:
```
python main.py
```

## Usage

Les informations récupérés sont pour l'instant:
- la tranche d'âge
- l'unité
- Le libellé du camp
- la date de début
- la date de fin
- le lieu
- le nombre de jeunes
- le nombre de chefs
- le directeur
- les alertes de MonProjet
- les warnings de MonProjet

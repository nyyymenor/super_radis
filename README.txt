# Simulation résolution de la chaleur dans un cylindre en 1D par différence finie

## Dépendances

Le script nécessite les packages suivants :
- numpy
- matplotlib
- tabulate

Ces dépendances sont vérifiées et installées automatiquement par le script.
Il est nécessaire d'avoir python > 3.6, être en dehors d'un venv, et avoir la possibilité de faire des pip install. Le script se charge de créer un venv et d'installer les modules. (A ne pas faire dans un environnement industriel mais pratique dans ce cas précis pour un one click button)
Testé sur W11 et python 3.12, devrait être fonctionnel sur environnement linux.

## Utilisation

Pour exécuter le script, utilisez la commande suivante :
python script.py

## Paramètres
Les paramètres de la simulation sont stockés dans le fichier parametres.json

## Résultats
Les résultats de la simulation sont enregistrés dans le fichier resultats.txt sous forme de tableau et un graphique (peut-être deux ?) est généré.


"""
Nom du module : Simulation résolution de la chaleur dans un cylindre en 1D par différence finie
Auteur : Jérémy CALLOT
"""

import json
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def lire_parametres(fichier = 'parametres.json'):
    """
    Cette fonction lit les paramètres du fichier 'parametres.json'.
    Elle retourne un dictionnaire contenant tous les paramètres.
    
    Args:
        fichier (str) : Adresse fichier input
    """
    with open(fichier, 'r', encoding='utf-8') as f:
        params = json.load(f)
    return params

def resoudre_equation(params):
    """
    Cette fonction résout l'équation de la chaleur en utilisant les paramètres donnés.
    Elle retourne la matrice de température, les grilles radiale et temporelle, la température de fusion en Celsius et l'intervalle de sortie.

    Args:
        params (dict): Un dictionnaire contenant tous les paramètres nécessaires pour résoudre l'équation.
    """

    # Paramètres physiques
    egen = params['Paramètres physiques']['Densité de puissance (W/m^3)']
    t_surface = params['Paramètres physiques']['Température de surface (°C)'] + 273.15 # Conversion de t_surface en Kelvin
    cc = params['Paramètres physiques']['Capacité calorifique (J/kgK)']
    rho = params['Paramètres physiques']["Densité (kg/m^3)"]
    k_formula = params['Paramètres physiques']["Formule pour la conductivité thermique (W/mK)"]
    t_fusion = params['Paramètres physiques']["Température de fusion (K)"]

    # Paramètres de simulation
    r = params['Paramètres de simulation']['Rayon (m)']
    dt = params['Paramètres de simulation']['Pas de temps (s)']
    dr = params['Paramètres de simulation']['Pas de rayon (m)']
    t_final = params['Paramètres de simulation']['Temps final (s)']

    # Paramètres de sortie
    output_interval = params['Paramètres de sortie']["Intervalle de temps pour l'affichage dans le tableau (s)"]

    data = []
    def k(T):
        return eval(k_formula)

    # Grille radiale et temporelle
    r = np.arange(0, r+dr, dr)
    t = np.arange(0, t_final+dt, dt)

    # Initialisation de la matrice de température
    T = np.zeros((len(r), len(t)))

    # Conditions initiales et de bord
    T[:, :] = 20 + 273.15
    T[-1, :] = t_surface

    flag = True
    # Boucle sur le temps
    for j in range(len(t)-1):
        # Boucle sur le rayon
        for i in range(1, len(r)-1):
            a = T[i, j]
            b = dt*(k(a)/(rho*cc))*(T[i+1, j]-2*T[i, j]+T[i-1, j])/dr**2
            c = dt*egen/(rho*cc)
            T[i, j+1] = a + b + c
            if T[i, j+1] > t_fusion and flag:
                print ("\n\nça chauffe ! On viens de dépasser la température de fusion (" + str(t_fusion) + " K) ! On est perdu hors domaine !")
                flag = False

        # Condition aux limites pour r=0
        T[0, j+1] = T[1, j+1] - dr*(T[2,j+1]-T[1,j+1])/(2*dr)
        
        # Enregistrement des résultats intermédiaires toutes les 10 secondes
        if t[j] % output_interval == 0:
            data.append([t[j]] + list(T[:, j+1] - 273.15))

    return T, r, t, t_fusion, data

def post_traitement(T, r, t, t_fusion, data):
    """
    Cette fonction effectue le post-traitement des résultats de la résolution de l'équation.
    Elle génère des graphiques et enregistre les résultats dans un fichier texte.
    
    Args:
        T (np.array): La matrice de température.
        r (np.array): La grille radiale.
        t (np.array): La grille temporelle.
        t_fusion_c (float): La température de fusion en Celsius.
        data (list): Tableau de sortie
    """

    T -= 273.15
    t_fusion_c = t_fusion - 273.15

    # Ajout des en-têtes de colonne pour chaque rayon
    headers = ['Temps (s)'] + [f'Rayon = {ri*100:.1f} cm' for ri in r]

    # Conversion du tableau en une chaîne formatée avec tabulate
    table = tabulate(data, headers=headers, tablefmt='plain', floatfmt=".1f")

    # Enregistrement du tableau dans un fichier texte
    with open('resultats.txt', 'w', encoding='utf-8') as f:
        f.write(table)

    img = mpimg.imread('ressources/super_radis.jpg')

    plt.imshow(img)

    # Affichage de l'image
    plt.show(block=False)

    # Création de la grille 3D
    r_cyl, t_time = np.meshgrid(r, t)

    # Création de la figure 3D
    fig1 = plt.figure()  # Création d'une nouvelle figure
    ax = fig1.add_subplot(111, projection='3d')

    # Tracé de la surface
    surf = ax.plot_surface(r_cyl, t_time, T.T, cmap='viridis')

    # Ajout d'une barre de couleur pour la légende
    fig1.colorbar(surf)

    # Définition des labels
    ax.set_xlabel('Rayon (m)')
    ax.set_ylabel('Temps (s)')
    ax.set_zlabel('Température (°C)')

    # Vérification si la température maximale est égale à t_fusion - 200
    if np.max(T) >= t_fusion_c - 200:
        # Création d'un tableau de la même taille que T rempli avec la valeur t_fusion
        t_fusion_plane = np.full_like(r_cyl, t_fusion_c)

        # Tracé du plan à la valeur t_fusion
        ax.plot_surface(r_cyl, t_time, t_fusion_plane, alpha=0.5, color='r')

        # Ajout de l'étiquette "T fusion" au plan
        max_radius = np.max(r_cyl)
        max_t_time = np.max(t_time)
        ax.text(max_radius, max_t_time, t_fusion_c, "T fusion", color='red')

    # Affichage du graphique
    plt.show()

if __name__ == "__main__":
    params = lire_parametres()
    T, r, t, t_fusion_c, output_interval = resoudre_equation(params)
    post_traitement(T, r, t, t_fusion_c, output_interval)

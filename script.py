import os
import json

from ressources.create_custom_venv import setup_venv

REQUIRED_PACKAGES = [
    'numpy',
    'matplotlib',
    'tabulate']

#A commenter si l'environnement possède déjà ces modules et si ça ne fonctionne pas bien.
if not os.getenv('VENV_ACTIVE'):
    os.environ['VENV_ACTIVE'] = '1'
    venv_path = setup_venv(REQUIRED_PACKAGES)
    os.execl(venv_path, venv_path, __file__)



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tabulate import tabulate

data = []

# Lecture du fichier de paramètres
with open('parametres.json', 'r', encoding='utf-8') as f:
    params = json.load(f)

# Paramètres physiques
Egen = params['Paramètres physiques']['Densité de puissance (W/m^3)']
Tsurface = params['Paramètres physiques']['Température de surface (°C)'] + 273.15 # Conversion de Tsurface en Kelvin
cc = params['Paramètres physiques']['Capacité calorifique (J/kgK)']
rho = params['Paramètres physiques']["Densité (kg/m^3)"]
k_formula = params['Paramètres physiques']["Formule pour la conductivité thermique (W/mK)"]
T_fusion = params['Paramètres physiques']["Température de fusion (K)"]

# Paramètres de simulation
r = params['Paramètres de simulation']['Rayon (m)']
dt = params['Paramètres de simulation']['Pas de temps (s)']
dr = params['Paramètres de simulation']['Pas de rayon (m)']
t_final = params['Paramètres de simulation']['Temps final (s)']

# Paramètres de sortie
output_interval = params['Paramètres de sortie']["Intervalle de temps pour l'affichage dans le tableau (s)"]

def k(T):
    return eval(k_formula)


# Grille radiale et temporelle
r = np.arange(0, r+dr, dr)
t = np.arange(0, t_final+dt, dt)

# Initialisation de la matrice de température
T = np.zeros((len(r), len(t)))

# Conditions initiales et de bord
T[:, :] = 20 + 273.15
T[-1, :] = Tsurface

flag = True
# Boucle sur le temps
for j in range(len(t)-1):
    # Boucle sur le rayon
    for i in range(1, len(r)-1):
        a = T[i, j]
        b = dt*(k(a)/(rho*cc))*(T[i+1, j]-2*T[i, j]+T[i-1, j])/dr**2
        c = dt*Egen/(rho*cc)
        T[i, j+1] = a + b + c
        if T[i, j+1] > T_fusion and flag:
            print ("\n\nça chauffe ! On viens de dépasser la température de fusion (" + str(T_fusion) + " K) ! On est perdu hors domaine !")
            flag = False
        
    # Condition aux limites pour r=0
    T[0, j+1] = T[1, j+1] - dr*(T[2,j+1]-T[1,j+1])/(2*dr)
    
    # Enregistrement des résultats intermédiaires toutes les 10 secondes
    if t[j] % output_interval == 0:
        data.append([t[j]] + list(T[:, j+1] - 273.15))

# Conversion de la température en °C
T -= 273.15  
T_fusion_C = T_fusion - 273.15

# Ajout des en-têtes de colonne pour chaque rayon
headers = ['Temps (s)'] + [f'Rayon = {ri*100:.1f} cm' for ri in r]

# Conversion du tableau en une chaîne formatée avec tabulate
table = tabulate(data, headers=headers, tablefmt='plain', floatfmt=".1f")

# Enregistrement du tableau dans un fichier texte
with open('resultats.txt', 'w') as f:
    f.write(table)
    
img = mpimg.imread('ressources/super_radis.jpg')

fig2 = plt.figure()  # Création d'une nouvelle figure
plt.imshow(img)

# Affichage de l'image
plt.show(block=False)    
    
    
    
# Création de la grille 3D
R, Time = np.meshgrid(r, t)

# Création de la figure 3D
fig1 = plt.figure()  # Création d'une nouvelle figure
ax = fig1.add_subplot(111, projection='3d')

# Tracé de la surface
surf = ax.plot_surface(R, Time, T.T, cmap='viridis')

# Ajout d'une barre de couleur pour la légende
fig1.colorbar(surf)

# Définition des labels
ax.set_xlabel('Rayon (m)')
ax.set_ylabel('Temps (s)')
ax.set_zlabel('Température (°C)')

# Vérification si la température maximale est égale à T_fusion - 200
if np.max(T) >= T_fusion_C - 200:
    # Création d'un tableau de la même taille que T rempli avec la valeur T_fusion
    T_fusion_plane = np.full_like(R, T_fusion_C)
    
    # Tracé du plan à la valeur T_fusion
    ax.plot_surface(R, Time, T_fusion_plane, alpha=0.5, color='r')
    
    # Ajout de l'étiquette "T fusion" au plan
    max_radius = np.max(R)
    max_time = np.max(Time)
    ax.text(max_radius, max_time, T_fusion_C, "T fusion", color='red')

# Affichage du graphique
plt.show()
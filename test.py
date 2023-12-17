import numpy as np


def test_bordure_temperature():
    from script import resoudre_equation
    
    params = {
        'Paramètres physiques': {
            'Densité de puissance (W/m^3)': 1e6,
            'Température de surface (°C)': 20,
            'Capacité calorifique (J/kgK)': 1000,
            'Densité (kg/m^3)': 2700,
            'Formule pour la conductivité thermique (W/mK)': '0.01*T',
            'Température de fusion (K)': 933.47
        },
        'Paramètres de simulation': {
            'Rayon (m)': 0.01,
            'Pas de temps (s)': 0.01,
            'Pas de rayon (m)': 0.001,
            'Temps final (s)': 10
        },
        'Paramètres de sortie': {
            "Intervalle de temps pour l'affichage dans le tableau (s)": 1
        }
    }

    # Exécutez la fonction
    T, r, t, T_fusion_C, data = resoudre_equation(params)

    # Vérifiez que la température en bordure est égale à Tsurface
    Tsurface_K = params['Paramètres physiques']['Température de surface (°C)']
    assert np.allclose(T[-1, :], Tsurface_K), "La température en bordure ne reste pas à Tsurface"
    
def test_no_empty_variable():
    
    from script import lire_parametres
    
    params = lire_parametres()
    
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
    
    assert Egen, "Egen est vide"
    assert Tsurface, "Tsurface est vide"
    assert cc, "cc est vide"
    assert rho, "rho est vide"
    assert k_formula, "k_formula est vide"
    assert T_fusion, "T_fusion est vide"
    assert r, "r est vide"
    assert dt, "dt est vide"
    assert dr, "dr est vide"
    assert t_final, "t_final est vide"
    assert output_interval, "output_interval est vide"
    

if __name__ == "__main__":
    test_no_empty_variable()
    test_bordure_temperature()
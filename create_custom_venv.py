import os
import sys
import subprocess

def setup_venv(REQUIRED_PACKAGES):
    # Créer un environnement virtuel
    if not os.path.exists('ressources/custom_venv'):
        subprocess.call([sys.executable, '-m', 'venv', 'ressources/custom_venv'])

    pip_path = 'ressources/custom_venv\\Scripts\\pip' if os.name == 'nt' else 'ressources/custom_venv/bin/pip'

    # Obtenir la liste des packages installés
    installed_packages = str(subprocess.check_output([pip_path, 'list']))

    # Installer les packages nécessaires
    for package in REQUIRED_PACKAGES:
        if package not in installed_packages:
            print(f"Le package {package} n'est pas installé. Installation en cours...")
            subprocess.call([pip_path, 'install', package])
        else:
            print(f"Le package {package} est déjà installé.")


if __name__ == "__main__":
    REQUIRED_PACKAGES = [
    'numpy',
    'matplotlib',
    'tabulate',
    'pytest',
    'pylint',
    'scipy']
    
    setup_venv(REQUIRED_PACKAGES)
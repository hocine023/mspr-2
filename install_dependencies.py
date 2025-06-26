import subprocess
import sys

def install_packages(packages):
    """
    Installe les paquets donnés s'ils ne sont pas déjà installés.
    """
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installation de {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        else:
            print(f"{package} est déjà installé.")

if __name__ == "__main__":
    dependencies = [
        "requests",
        "dash",
        "pandas",
        "plotly",
        "flask",
        "werkzeug"
    ]
    install_packages(dependencies)
    print("Toutes les dépendances sont installées !")

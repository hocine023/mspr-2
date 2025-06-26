# Image de base officielle pour Flask
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exposer le port (par défaut utilisé par Flask)
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python", "app.py"]

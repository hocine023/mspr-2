FROM node:18

WORKDIR /app

# Étape 1 : copie des fichiers de dépendances
COPY package*.json ./

# Étape 2 : installation complète (vite y compris)
RUN npm install

# Étape 3 : copie du reste du projet (vite.config.js, src/, etc.)
COPY . .

# Étape 4 : expose le port pour Vite dev server
EXPOSE 5173

# Étape 5 : démarre l'app avec vite local
CMD ["npm", "run", "dev", "--", "--host"]

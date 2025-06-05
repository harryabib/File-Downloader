# File Downloader

## Installation et lancement

### Prérequis
- Docker
- Docker Compose

### Lancement rapide
```bash
# Cloner le repository
git clone https://github.com/harryabib/file-downloader.git
cd file-downloader

# Construire et lancer l'application
make up
```

L'application sera accessible sur : http://localhost:5000

*Des fichiers de test sont déjà inclus dans le dossier `files/`*

## Endpoints

- **GET `/`** - Interface web avec liste des fichiers
- **GET `/api/files`** - API JSON listant les fichiers
- **GET `/download/<filename>`** - Télécharge un fichier
- **GET `/health`** - Statut de l'application

## Exemples d'utilisation

### Lister les fichiers via API
```bash
curl http://localhost:5000/api/files
```

**Réponse :**
```json
[
  {
    "name": "hello.txt",
    "size": "13 octets",
    "modified": "2024-01-15 10:30:00",
    "type": "text/plain"
  }
]
```

## Tests

### Exécuter les tests
```bash
make test
```

### Tests inclus
- Test de l'endpoint `/health`
- Test de l'API `/api/files`
- Test de téléchargement de fichier
- Test des erreurs 404
- Test de la page d'accueil

## Commandes disponibles

```bash
make build     # Construire l'image Docker
make up        # Lancer l'application en arrière-plan
make down      # Arrêter l'application
make restart   # Redémarrer complètement l'application
make logs      # Voir les logs en temps réel
make test      # Exécuter les tests
make clean     # Nettoyer complètement (conteneurs, volumes, images)
```

---
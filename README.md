**Formation** : Monitoring & Observabilité avec Prometheus et Grafana  
**Stack technique** : FastAPI + Prometheus + Grafana + PostgreSQL + Docker

---

## 📁 Structure du Projet

```
monitoring-fastapi/
├── app/
│   ├── main.py                     # Application FastAPI principale
│   ├── routes/
│   │   └── items.py                # Routes CRUD instrumentées
│   ├── monitoring/
│   │   └── metrics.py              # Définition des métriques
│   └── database.py                 # Configuration DB
├── prometheus/
│   └── prometheus.yml              # Configuration Prometheus
├── grafana/
│   └── dashboards/                 # Dashboards exportés (JSON)
│       ├── vue-ensemble-http.json
│       ├── metriques-metier.json
│       ├── performance-bdd.json
│       └── metriques-red.json
├── screenshots/
│   └── grafana/                    # Captures d'écran dashboards
│       ├── dashboard-http.png
│       ├── dashboard-metier.png
│       ├── dashboard-bdd.png
│       └── dashboard-red.png
├── docker-compose.yml              # Stack complète
├── Dockerfile                      # Image FastAPI
├── locustfile.py                   # Tests de charge (optionnel)
└── RENDU_MONITORING.md             # Ce fichier
```

## 🛠️ Installation et Utilisation

### Prérequis

```bash
# Versions utilisées
Docker 24+
Docker Compose 2.20+
Python 3.11+
```

### Démarrage de la stack

```bash
# Cloner le projet
git clone https://github.com/Malek-Boumedine/brief_monitoring
cd monitoring-fastapi

# Lancer la stack complète
docker compose up -d

# Vérifier les services
docker compose ps
```

### Accès aux services

| Service | URL | Credentials |
|---------|-----|-------------|
| **FastAPI** | http://localhost:8000 | - |
| **API Docs** | http://localhost:8000/docs | - |
| **Métriques** | http://localhost:8000/metrics | - |
| **Prometheus** | http://localhost:9090 | - |
| **Grafana** | http://localhost:3000 | admin / admin |

### Générer du trafic

```bash
# Méthode 1 : Tests manuels via Swagger UI
# Ouvrir http://localhost:8000/docs et faire des requêtes

# Méthode 2 : Script de génération
curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d '{"nom":"Test","prix":10.5}'
curl http://localhost:8000/items

# Méthode 3 : Locust (si installé)
locust -f locustfile.py
# Ouvrir http://localhost:8089
```

---

## 📸 Captures d'écran des Dashboards

### Vue d'ensemble HTTP
![Dashboard HTTP](screenshots/grafana/dashboard-http.png)

### Métriques métier
![Dashboard Métier](screenshots/grafana/dashboard-metier.png)

### Performance base de données
![Dashboard BDD](screenshots/grafana/dashboard-bdd.png)

### Métriques RED
![Dashboard RED](screenshots/grafana/dashboard-red1.png)

![Dashboard RED](screenshots/grafana/dashboard-red2.png)
---


# 📚 Veille sur l'Observabilité - Phase 0

**Auteur :** [Ton nom]  
**Date :** 26 décembre 2025  
**Formation :** Brief Monitoring & Observabilité (14h)

---

## 🎯 Objectif de la veille

Cette veille a pour but de comprendre les concepts fondamentaux de l'observabilité, les différences avec le monitoring traditionnel, et les outils Prometheus/Grafana utilisés pour implémenter une solution de monitoring moderne.

---

## 1️⃣ Monitoring vs Observabilité : Quelle différence ?

### Définitions

**Monitoring** : Approche réactive qui consiste à surveiller des métriques prédéfinies et à lever des alertes lorsque des seuils sont dépassés.

**Observabilité** : Approche proactive qui permet de comprendre l'état interne d'un système à partir de ses sorties (métriques, logs, traces), facilitant l'investigation et le debugging.

### Comparaison

| Critère | Monitoring | Observabilité |
|---------|-----------|---------------|
| **Question** | "L'app est-elle up ?" | "Pourquoi cette requête est lente ?" |
| **Approche** | Réactive - Attendre une alerte | Proactive - Investigation libre |
| **Outils** | Dashboards fixes, alertes prédéfinies | Exploration ad-hoc, corrélation |
| **Métaphore** | Tableau de bord de voiture | Boîte noire d'avion |

### Points clés

- Le monitoring est un **sous-ensemble** de l'observabilité
- Le monitoring indique **QUAND** un problème survient
- L'observabilité explique **POURQUOI** le problème est survenu
- On ne peut pas avoir d'observabilité sans monitoring, mais on peut avoir du monitoring sans observabilité complète

---

## 2️⃣ Les 3 piliers de l'observabilité

### Pilier 1 : Métriques 📊

**Définition** : Données numériques agrégées dans le temps, représentant l'état d'un système.

**Exemples** :
- CPU : 45%
- Mémoire RAM : 2.3 GB / 8 GB
- Requêtes HTTP/seconde : 1250 req/s
- Latence P95 : 120ms
- Erreurs 5xx : 12 en 5 minutes

**Avantages** :
- Léger en stockage
- Permet des tendances et graphiques
- Alertes faciles à configurer

**Cas d'usage** : Dashboards temps réel, alerting, capacity planning

---

### Pilier 2 : Logs 📝

**Définition** : Événements textuels horodatés décrivant ce qui se passe dans l'application.

**Exemple** :
```
2025-01-15 10:23:45 INFO  [api] User 42 logged in successfully
2025-01-15 10:23:47 ERROR [db]  Connection pool exhausted (timeout: 30s)
2025-01-15 10:23:48 WARN  [api] Retry attempt 1/3 for user 42
```

**Avantages** :
- Contexte détaillé (stack traces, user IDs)
- Debugging précis

**Cas d'usage** : Investigation d'erreurs, audit, debugging

---

### Pilier 3 : Traces 🔍

**Définition** : Suivi d'une requête à travers plusieurs services (distributed tracing).

**Exemple** :
```
Request ID: #12345 | Total: 177ms
├─ API Gateway      →  5ms
├─ Auth Service     → 12ms
├─ Items API        → 50ms
│  ├─ DB Query      → 120ms  ⚠️ SLOW!
│  └─ Cache Check   →   5ms
└─ Response         →  5ms
```

**Avantages** :
- Vue end-to-end d'une requête
- Identifie le service lent dans une chaîne

**Cas d'usage** : Microservices, systèmes distribués

**Note** : Cette formation se concentre sur les **MÉTRIQUES** (le pilier le plus accessible et fondamental).

---

## 3️⃣ Qu'est-ce que Prometheus ?

### Définition

Prometheus est une base de données time-series open-source spécialisée dans le stockage et l'interrogation de métriques.

### Architecture : Pull vs Push

**Architecture Pull (Prometheus)** :
- Prometheus scrape (interroge) régulièrement l'endpoint `/metrics` de l'application
- Fréquence configurable (par défaut : 15 secondes)
- L'application n'a pas besoin de connaître Prometheus
- Détection automatique si l'app est down

**Architecture Push (ex: StatsD)** :
- L'application envoie activement les métriques vers un collecteur
- L'app doit connaître l'adresse du collecteur
- Peut surcharger le réseau

### Caractéristiques principales

| Caractéristique | Détail |
|-----------------|--------|
| 🗄️ Base time-series | Stocke (timestamp, valeur) |
| ⬅️ Pull HTTP | Scrape `/metrics` toutes les 15s |
| 📊 Format texte | Simple, lisible par un humain |
| 🔍 PromQL | Langage de requête puissant |
| ⏱️ Rétention | Configurable (par défaut 15 jours) |
| 💾 Stockage local | Pas de dépendance externe |

---

## 4️⃣ Les 4 types de métriques Prometheus

### Counter 📊

**Définition** : Valeur qui ne fait qu'augmenter (sauf redémarrage de l'application).

**Comportement** : ⬆️ Monotone croissant

**Exemples** :
```python
http_requests_total{method="GET", status="200"} 45678
```

**Cas d'usage** :
- Nombre total de requêtes HTTP
- Nombre d'erreurs
- Nombre d'utilisateurs inscrits

**Important** : Pour obtenir un taux par seconde, utiliser `rate()` dans PromQL :
```promql
rate(http_requests_total[5m])  # Requêtes par seconde sur 5 min
```

---

### Gauge 📈

**Définition** : Valeur qui peut monter ET descendre (mesure instantanée).

**Comportement** : ⬆️⬇️ Peut varier dans les deux sens

**Exemples** :
```python
memory_usage_bytes 2684354560  # 2.5 GB
cpu_usage_percent 45.2
active_connections 127
```

**Cas d'usage** :
- Utilisation mémoire/CPU
- Nombre de connexions actives
- Température serveur
- File d'attente (queue size)

**Important** : Utiliser directement la valeur, pas besoin de `rate()`

---

### Histogram ⏱️

**Définition** : Distribution de valeurs réparties dans des intervalles (buckets).

**Comportement** : 📊 Répartit les observations dans des buckets prédéfinis

**Exemple** :
```python
http_request_duration_seconds_bucket{le="0.1"} 8234    # < 100ms
http_request_duration_seconds_bucket{le="0.5"} 9876    # < 500ms
http_request_duration_seconds_bucket{le="1.0"} 10234   # < 1s
http_request_duration_seconds_bucket{le="+Inf"} 10500  # Total
```

**Cas d'usage** :
- Latences HTTP
- Temps de requête DB
- Tailles de réponses

**Avantage** : Permet de calculer les percentiles avec `histogram_quantile()` :
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
# P95 : 95% des requêtes sont plus rapides que cette valeur
```

---

### Summary 📉

**Définition** : Similaire à Histogram mais avec percentiles précalculés côté application.

**Comportement** : 📈 Calcule P50, P90, P95, P99 à la source

**Exemple** :
```python
http_request_duration_seconds{quantile="0.5"} 0.12   # P50 (médiane)
http_request_duration_seconds{quantile="0.95"} 0.45  # P95
http_request_duration_seconds{quantile="0.99"} 1.2   # P99
```

**Différence avec Histogram** :

| Critère | Histogram | Summary |
|---------|-----------|---------|
| Calcul | Côté Prometheus (PromQL) | Côté application |
| Flexibilité | ✅ Peut changer les percentiles | ❌ Percentiles fixes |
| Performance | ✅ Léger côté app | ❌ Plus lourd côté app |
| Agrégation | ✅ Peut agréger plusieurs instances | ❌ Difficile à agréger |

**Recommandation** : Préférer **Histogram** en général.

---

## 5️⃣ Découverte de Grafana

### Définition

Grafana est un outil de visualisation open-source qui transforme les métriques en dashboards interactifs et esthétiques.

### Rôle dans la stack

```
Prometheus → Collecte et stocke les métriques
     ↓
  Grafana → Visualise les métriques
```

### Fonctionnalités principales

| Fonctionnalité | Description |
|----------------|-------------|
| 📊 Dashboards | Tableaux de bord personnalisables |
| 🔌 Multi-sources | Prometheus, InfluxDB, MySQL, etc. |
| 📈 Visualisations | Time series, Gauge, Stat, Heatmap, Pie chart |
| 🚨 Alerting | Notifications Slack, Email, etc. |
| 👥 Collaboration | Partage de dashboards |

### Types de visualisations

- **Time series** : Courbes temporelles (ex: CPU over time)
- **Gauge** : Jauge visuelle (ex: Disk usage: 45%)
- **Stat** : Valeur numérique avec seuils de couleur
- **Heatmap** : Carte de chaleur (ex: distribution latences)
- **Pie chart** : Camembert (ex: répartition requêtes par endpoint)

---

## 📚 Mission 1 : Comprendre PromQL (15min)

### Questions explorées

#### 1. Quelle est la différence entre `rate()` et `increase()` ?

**`rate()`** :
- Calcule le **taux moyen par seconde** sur une période donnée
- Retourne une valeur par seconde
- Utilisé pour les graphiques de tendances
- Exemple : `rate(http_requests_total[5m])` → requêtes/seconde

**`increase()`** :
- Calcule l'**augmentation totale** sur une période donnée
- Retourne une valeur absolue
- Utilisé pour connaître l'augmentation brute
- Exemple : `increase(http_requests_total[1h])` → nombre total de requêtes en 1h

**En résumé** : `increase()` = `rate()` × durée de la fenêtre

---

#### 2. Comment filtrer des métriques par label ?

**Syntaxe de base** :
```promql
metric_name{label="value"}
```

**Exemples** :
```promql
# Filtrer par status code exact
http_requests_total{status="200"}

# Filtrer par méthode HTTP
http_requests_total{method="GET"}

# Filtrer par regex (codes 5xx)
http_requests_total{status=~"5.."}

# Exclure un label
http_requests_total{status!="200"}

# Combiner plusieurs filtres
http_requests_total{method="POST", status="201"}
```

---

#### 3. Que fait la fonction `histogram_quantile()` ?

**Fonction** : Calcule un percentile (quantile) à partir d'un histogram.

**Syntaxe** :
```promql
histogram_quantile(φ, rate(metric_bucket[range]))
```

Où `φ` est le percentile souhaité (0.5 = P50, 0.95 = P95, 0.99 = P99)

**Exemple** :
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

**Signification** : "95% des requêtes ont une latence inférieure à cette valeur"

**Percentiles courants** :
- P50 (médiane) : La moitié des requêtes sont plus rapides
- P95 : 95% des requêtes sont plus rapides (utilisé pour les SLOs)
- P99 : 99% des requêtes sont plus rapides (détecte les cas extrêmes)

---

## 📚 Mission 2 : Best Practices Prometheus (15min)

### 1. Comment nommer correctement une métrique ?

**Format recommandé** :
```
<namespace>_<subsystem>_<name>_<unit>
```

**Exemples** :
```
# ✅ Bon
http_requests_total
http_request_duration_seconds
db_connections_active
items_created_total

# ❌ Mauvais
requestsTotal
http-requests
requests_number
```

**Règles** :
- Utiliser le **snake_case**
- Inclure l'**unité** dans le nom (seconds, bytes, total, etc.)
- Suffixe `_total` pour les Counters
- Suffixe `_seconds` pour les durées
- Préfixer par le domaine (`http_`, `db_`, `cache_`)

---

### 2. Quand utiliser des labels vs créer plusieurs métriques ?

**Utiliser des labels** :
- Pour des **dimensions variables** (endpoint, status code, user type)
- Lorsque les valeurs sont **prévisibles et limitées**
- Pour permettre l'agrégation et le filtrage

**Exemple** :
```python
# ✅ Bon - Un compteur avec labels
http_requests_total{method="GET", status="200", endpoint="/items"}
http_requests_total{method="POST", status="201", endpoint="/items"}

# ❌ Mauvais - Plusieurs compteurs séparés
http_requests_get_items_200_total
http_requests_post_items_201_total
```

**Créer plusieurs métriques** :
- Pour des **types de mesures différentes** (latence vs nombre de requêtes)
- Pour des **unités différentes** (bytes vs seconds)

**⚠️ Attention** : Éviter les labels avec une **cardinalité élevée** (ex: user_id, request_id) car cela explose le nombre de séries temporelles.

---

### 3. Quels sont les dashboards anti-patterns à éviter ?

**Anti-pattern 1 : Trop d'informations**
- ❌ 20+ panels sur un seul dashboard
- ✅ Diviser en plusieurs dashboards thématiques

**Anti-pattern 2 : Pas de contexte**
- ❌ Graphiques sans titre, sans unité, sans légende
- ✅ Titres clairs, unités explicites, légendes lisibles

**Anti-pattern 3 : Graphiques non adaptés**
- ❌ Utiliser un pie chart pour des séries temporelles
- ✅ Time series pour les tendances, Gauge pour les valeurs instantanées

**Anti-pattern 4 : Requêtes lourdes**
- ❌ Requêtes complexes avec de longues périodes (1 an)
- ✅ Limiter la période et optimiser les requêtes

**Anti-pattern 5 : Pas de seuils**
- ❌ Graphiques sans indication de "normal" vs "problématique"
- ✅ Définir des seuils de couleur (vert/jaune/rouge)

**Anti-pattern 6 : Dashboards non maintenus**
- ❌ Panels cassés, métriques obsolètes
- ✅ Réviser et nettoyer régulièrement

---

## ✅ Auto-évaluation

### Concepts compris

- [x] La différence entre monitoring et observabilité
- [x] Les 3 piliers de l'observabilité (métriques, logs, traces)
- [x] Pourquoi Prometheus utilise le Pull (contrôle, simplicité, détection de pannes)
- [x] Quand utiliser Counter vs Gauge vs Histogram
  - Counter : pour compter des événements cumulés
  - Gauge : pour des valeurs instantanées qui varient
  - Histogram : pour mesurer des distributions (latences)
- [x] Le rôle de Grafana dans la stack (visualisation des métriques collectées par Prometheus)

### Questions du quiz

1. **Monitoring vs Observabilité : quelle différence ?**
   - Monitoring = réactif, alertes prédéfinies, répond à "QUAND"
   - Observabilité = proactif, investigation libre, répond à "POURQUOI"

2. **Citez les 3 piliers de l'observabilité**
   - Métriques (données numériques agrégées)
   - Logs (événements textuels horodatés)
   - Traces (suivi de requêtes distribuées)

3. **Quel type de métrique pour compter les requêtes HTTP ?**
   - **Counter** (valeur qui ne fait qu'augmenter)

4. **Quel type de métrique pour l'utilisation RAM actuelle ?**
   - **Gauge** (valeur instantanée qui varie)

5. **Que signifie P95 ?**
   - Percentile 95 : 95% des observations sont inférieures ou égales à cette valeur
   - Utilisé pour mesurer les performances tout en ignorant les outliers extrêmes

---

## 📚 Ressources consultées

### Documentation officielle
- [Prometheus - Query Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Prometheus Best Practices - Naming](https://prometheus.io/docs/practices/naming/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)

### Vidéos
- [YouTube : Prometheus & Grafana Tutorial](https://youtu.be/TQQhm_kNuQY)
- Recherche : "PromQL tutorial" pour approfondir

### Lectures complémentaires
- [Red Hat - Qu'est-ce que l'observabilité ?](https://www.redhat.com/fr/topics/devops/what-is-observability)
- [OpenTelemetry - Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/)

---

## 🎯 Conclusion de la veille

Cette phase de veille m'a permis de :
- Comprendre les différences fondamentales entre monitoring et observabilité
- Identifier les 3 piliers de l'observabilité et leur rôle respectif
- Découvrir Prometheus et son architecture Pull
- Maîtriser les 4 types de métriques et leurs cas d'usage
- Apprendre les bases de PromQL (rate, increase, histogram_quantile)
- Connaître les bonnes pratiques de nommage et d'organisation

**Prêt pour la suite** : Instrumentation de l'application FastAPI avec des métriques Prometheus ! 🚀

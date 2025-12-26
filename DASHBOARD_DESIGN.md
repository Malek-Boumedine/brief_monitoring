# Design de mes Dashboards - Projet Monitoring

> **Note** : Ce document récapitule la conception des 4 dashboards Grafana créés pour le projet de monitoring FastAPI.

---

## Dashboard 1 : Vue d'ensemble HTTP

### Objectif
Fournir une vision globale de la santé et des performances de l'API FastAPI en temps réel. Ce dashboard permet de détecter rapidement les anomalies (erreurs, latence élevée) et de surveiller le trafic HTTP global.

### Public cible
- **Équipe Ops/SRE** : Surveillance 24/7 de la disponibilité
- **Développeurs** : Détection rapide des régressions de performance
- **Management technique** : Vue d'ensemble de la santé de l'application

### Métriques clés à afficher

1. **Requêtes totales par seconde** - Pourquoi : Indicateur principal de charge et d'utilisation de l'API
2. **Temps de réponse P95** - Pourquoi : Mesure la latence ressentie par 95% des utilisateurs (SLI critique)
3. **Taux d'erreurs 5xx (%)** - Pourquoi : Indicateur de fiabilité et stabilité de l'application
4. **Requêtes actives** - Pourquoi : Détecte les problèmes de concurrence et les requêtes bloquées

### Disposition prévue

```
┌─────────────────────────────────────────────────────────┐
│  Dashboard: Vue d'ensemble HTTP                         │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────┐  ┌──────────────────────┐    │
│  │ Requêtes totales     │  │ Taux d'erreurs 5xx   │    │
│  │ (Time Series)        │  │ (Stat avec seuils)   │    │
│  │                      │  │  🟢 < 1%             │    │
│  │  📈 Courbe           │  │  🟡 1-5%             │    │
│  │     temporelle       │  │  🔴 > 5%             │    │
│  └──────────────────────┘  └──────────────────────┘    │
│                                                           │
│  ┌──────────────────────┐  ┌──────────────────────┐    │
│  │ Temps de réponse P95 │  │ Requêtes actives     │    │
│  │ (Time Series)        │  │ (Gauge)              │    │
│  │                      │  │                      │    │
│  │  📈 Latence par      │  │   🎯 Jauge visuelle  │    │
│  │     endpoint         │  │                      │    │
│  └──────────────────────┘  └──────────────────────┘    │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

**Visualisations** : 2x Time Series, 1x Stat, 1x Gauge  
**Queries PromQL** : 4 requêtes principales  
**Refresh** : 10s

---

## Dashboard 2 : Métriques métier

### Objectif
Suivre l'activité métier de l'application en mesurant les opérations CRUD sur les items. Ce dashboard répond aux questions : "Combien d'items sont créés/lus/modifiés/supprimés ?" et "Quelle est la tendance d'utilisation ?".

### Public cible
- **Product Managers** : Comprendre l'usage de l'application
- **Business Analysts** : Analyser les tendances d'activité
- **Développeurs** : Valider le comportement métier

### Métriques clés à afficher

1. **Opérations CRUD par seconde** - Pourquoi : Mesure l'activité métier en temps réel
2. **Total cumulé par type d'opération** - Pourquoi : Vue globale depuis le démarrage
3. **Répartition par méthode HTTP** - Pourquoi : Équilibre GET/POST/PUT/DELETE
4. **Tendance lecture vs écriture** - Pourquoi : Identifier les patterns d'usage

### Disposition prévue

```
┌─────────────────────────────────────────────────────────┐
│  Dashboard: Métriques métier                            │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Opérations CRUD par seconde (Time Series multi)    │ │
│  │                                                     │ │
│  │  📊 4 courbes superposées :                        │ │
│  │     • Créations (bleu)                             │ │
│  │     • Lectures (vert)                              │ │
│  │     • Mises à jour (orange)                        │ │
│  │     • Suppressions (rouge)                         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌─────────┐│
│  │ Total     │ │ Total     │ │ Total     │ │ Total   ││
│  │ Créations │ │ Lectures  │ │ Updates   │ │ Deletes ││
│  │ (Stat)    │ │ (Stat)    │ │ (Stat)    │ │ (Stat)  ││
│  │  🔢 1234  │ │  🔢 5678  │ │  🔢 432   │ │ 🔢 89   ││
│  └───────────┘ └───────────┘ └───────────┘ └─────────┘│
│                                                           │
│  ┌──────────────────────┐  ┌──────────────────────┐    │
│  │ Répartition par      │  │ Ratio Lecture/       │    │
│  │ méthode HTTP         │  │ Écriture             │    │
│  │ (Pie Chart)          │  │ (Time Series)        │    │
│  │                      │  │                      │    │
│  │  🥧 GET: 60%         │  │  📈 Tendance         │    │
│  │     POST: 20%        │  │                      │    │
│  │     PUT: 15%         │  │                      │    │
│  │     DELETE: 5%       │  │                      │    │
│  └──────────────────────┘  └──────────────────────┘    │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

**Visualisations** : Time Series, Stat (grid 4x), Pie Chart  
**Queries PromQL** : 8+ requêtes  
**Refresh** : 15s

---

## Dashboard 3 : Performance base de données

### Objectif
Identifier les goulots d'étranglement au niveau base de données en surveillant la latence des requêtes SQL et la santé du pool de connexions. Dashboard critique pour l'optimisation des performances.

### Public cible
- **Développeurs backend** : Optimisation des requêtes SQL
- **DBAs** : Surveillance de la charge DB
- **SRE** : Détection des problèmes de performance

### Métriques clés à afficher

1. **Distribution des latences DB (Heatmap)** - Pourquoi : Visualise la répartition complète des temps de réponse DB
2. **Latence DB (P50/P95/P99)** - Pourquoi : Mesure la performance perçue (médiane, percentiles élevés)
3. **Pool de connexions** - Pourquoi : Détecte la saturation du pool
4. **Requêtes lentes (>100ms)** - Pourquoi : Identifie les queries à optimiser

### Disposition prévue

```
┌─────────────────────────────────────────────────────────┐
│  Dashboard: Performance base de données                 │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Distribution des latences DB (Heatmap)             │ │
│  │                                                     │ │
│  │  🔥 Carte de chaleur :                             │ │
│  │     Temps (axe X) x Latence (axe Y)                │ │
│  │     Couleur = Densité de requêtes                  │ │
│  │                                                     │ │
│  │     Plus de requêtes ─────────► Plus rouge        │ │
│  │     Moins de requêtes ────────► Plus bleu         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Latence DB - P50/P95/P99 (Time Series multi)      │ │
│  │                                                     │ │
│  │  📊 3 courbes :                                    │ │
│  │     • P50 (médiane) - vert                         │ │
│  │     • P95 - orange                                 │ │
│  │     • P99 - rouge                                  │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌──────────────────────┐  ┌──────────────────────┐    │
│  │ Pool de connexions   │  │ Requêtes lentes      │    │
│  │ (Gauge)              │  │ >100ms (Stat)        │    │
│  │                      │  │                      │    │
│  │   🎯 12 / 20         │  │  ⚠️  23 req/s        │    │
│  │      connexions      │  │                      │    │
│  └──────────────────────┘  └──────────────────────┘    │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

**Visualisations** : Heatmap, Time Series multi, Gauge, Stat  
**Queries PromQL** : 6 requêtes  
**Refresh** : 10s

---

## Dashboard 4 : Métriques RED

### Objectif
Appliquer la méthodologie RED (Rate, Errors, Duration) pour chaque endpoint de l'API. Ce dashboard permet de détecter rapidement quel endpoint a des problèmes de performance ou génère des erreurs.

### Public cible
- **Développeurs** : Debugging et optimisation par endpoint
- **SRE** : Monitoring orienté SLO/SLI
- **DevOps** : Suivi des déploiements et régressions

### Métriques clés à afficher

1. **Rate - Requêtes par endpoint** - Pourquoi : Identifier les endpoints les plus sollicités
2. **Errors - Taux d'erreur par endpoint** - Pourquoi : Détecter les endpoints problématiques
3. **Duration - Latence P95 par endpoint** - Pourquoi : Identifier les endpoints lents
4. **Top endpoints les plus lents** - Pourquoi : Prioriser les optimisations

### Disposition prévue

```
┌─────────────────────────────────────────────────────────┐
│  Dashboard: Métriques RED (Rate, Errors, Duration)     │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │ RATE - Requêtes par endpoint (Time Series)        │ │
│  │                                                     │ │
│  │  📈 Courbes par endpoint :                         │ │
│  │     • GET /items                                   │ │
│  │     • POST /items                                  │ │
│  │     • GET /items/{id}                              │ │
│  │     • PUT /items/{id}                              │ │
│  │     • DELETE /items/{id}                           │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │ ERRORS - Taux d'erreur par endpoint (Time Series) │ │
│  │                                                     │ │
│  │  📊 % d'erreurs 5xx par endpoint                   │ │
│  │     Seuil d'alerte : > 1%                          │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │ DURATION - Latence P95 par endpoint (Time Series) │ │
│  │                                                     │ │
│  │  ⏱️  Temps de réponse P95 :                        │ │
│  │     Permet de comparer la performance relative     │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Top endpoints les plus lents (Table ou Stat)      │ │
│  │                                                     │ │
│  │  🏆 Classement par latence moyenne                 │ │
│  │     1. PUT /items/{id}      → 450ms                │ │
│  │     2. POST /items          → 280ms                │ │
│  │     3. GET /items/{id}      → 120ms                │ │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

**Visualisations** : 3x Time Series (multi-séries), Table/Stat  
**Queries PromQL** : 4-5 requêtes avec filtres `by (handler)`  
**Refresh** : 10s

---

## 🎨 Principes de Design Appliqués

### Organisation spatiale
- ✅ **Métriques critiques en haut** : Taux d'erreur, requêtes/s toujours visibles
- ✅ **Stats simples d'abord** : Chiffres clés avant les graphiques détaillés
- ✅ **Regroupement logique** : Métriques liées côte à côte
- ✅ **Largeur adaptée** : Panels larges pour Time Series, grilles pour Stats

### Couleurs et seuils
- 🟢 **Vert** : Tout va bien (latence < 200ms, erreurs < 1%)
- 🟡 **Jaune/Orange** : Attention (latence 200-500ms, erreurs 1-5%)
- 🔴 **Rouge** : Problème (latence > 500ms, erreurs > 5%)
- 🔵 **Bleu** : Neutre (métriques sans seuil)

### Légendes
- ✅ **Dynamiques** : `{{method}} {{handler}}` pour adapter aux données
- ✅ **Fixes** : Titres clairs pour les métriques simples
- ✅ **Masquées** : Sur les heatmaps (couleurs suffisent)

### Unités
- ✅ **req/s** : Taux de requêtes
- ✅ **seconds (s)** : Latences (converti en ms par Grafana si < 1s)
- ✅ **Percent (0-100)** : Taux d'erreur
- ✅ **Aucune** : Compteurs bruts (total items created)

---

## 📊 Récapitulatif des Visualisations

| Dashboard | Time Series | Stat | Gauge | Pie | Heatmap | Table | Total Panels |
|-----------|-------------|------|-------|-----|---------|-------|--------------|
| **HTTP Overview** | 2 | 1 | 1 | - | - | - | **4** |
| **Métriques métier** | 2 | 4 | - | 1 | - | - | **7** |
| **Performance BDD** | 1 | 1 | 1 | - | 1 | - | **4** |
| **RED** | 3 | 1-2 | - | - | - | 0-1 | **4-6** |
| **TOTAL** | **8** | **7-8** | **2** | **1** | **1** | **0-1** | **19-21** |

✅ **Contrainte "3 types minimum"** : Largement dépassée (5-6 types)  
✅ **Contrainte "6 panels minimum"** : 19-21 panels au total  
✅ **Métriques custom** : Toutes les métriques CRUD utilisées

---

## 🚀 Approche Choisie

**Approche hybride "Overview + RED + Business"** :

1. **Dashboard 1** : Vue d'ensemble SRE (disponibilité, santé globale)
2. **Dashboard 2** : Métriques business (activité métier)
3. **Dashboard 3** : Performance technique (optimisation)
4. **Dashboard 4** : RED methodology (debugging par endpoint)

Cette approche couvre **tous les besoins** :
- ✅ Opérationnel (Ops/SRE)
- ✅ Métier (Product/Business)
- ✅ Technique (Dev/Perf)
- ✅ Debugging (RED)

---

## ✅ Validation des Contraintes

- [x] **Minimum 6 panels** → **19-21 panels créés** ✅
- [x] **3 types de visualisation minimum** → **5-6 types utilisés** ✅
- [x] **1 panel avec plusieurs queries** → Multiples (CRUD ops, P50/P95/P99, etc.) ✅
- [x] **1 métrique custom** → Toutes les métriques CRUD custom ✅
- [x] **Titres clairs** → Tous les panels ont des titres descriptifs ✅
- [x] **Unités appropriées** → req/s, ms, %, etc. configurées ✅
- [x] **Légendes personnalisées** → Dynamiques et fixes selon contexte ✅

---


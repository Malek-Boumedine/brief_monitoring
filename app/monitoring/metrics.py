"""
Module de métriques Prometheus pour l'API Items
EXEMPLE DE CODE avec annotations pédagogiques
"""

from prometheus_client import Counter, Histogram, Gauge, Info
import time

# ℹ️ INFO : Informations statiques sur l'application
app_info = Info(
    'fastapi_app_info',
    'Information about the FastAPI application'
)

# 📊 COUNTER : Compteur unique avec labels pour le CRUD
items_operations_total = Counter(
    'items_operations_total',
    'Nombre total d\'opérations sur les items',
    ['operation', 'status']
)

# 📈 GAUGE : Valeur instantanée
db_connection_pool_size = Gauge(
    'db_connection_pool_size',
    'Taille actuelle du pool de connexions DB'
)

# ⏱️ HISTOGRAM : Distribution de valeurs avec buckets
db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Durée des requêtes base de données (secondes)',
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

# 🎯 Context Manager pour mesurer automatiquement les durées
class DatabaseQueryTimer:
    """Context manager pour mesurer le temps d'exécution d'une requête DB."""

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.perf_counter() - self.start_time
        db_query_duration_seconds.observe(duration)

# 💡 Note : Vous pouvez maintenant utiliser le compteur ainsi :
# items_operations_total.labels(operation='create', status='success').inc()
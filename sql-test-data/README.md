# PostgreSQL DBA Multi-Agent - Test Data SQL Scripts

Scripts SQL pour alimenter votre base PostgreSQL avec des données de test réalistes qui démontreront toutes les capacités de votre système DBA multi-agent.

## 🎯 Objectif

Créer des scénarios de base de données réalistes qui déclencheront et montreront :

- **Problèmes de Performance** : Requêtes lentes, sessions bloquantes, problèmes d'index
- **Vulnérabilités de Sécurité** : Contrôles d'accès faibles, authentification faible
- **Problèmes de Schéma** : Tables bloatées, index manquants, anti-patterns de conception
- **Besoins de Maintenance** : Exigences VACUUM, problèmes de configuration

## 🚀 Utilisation Rapide

```bash
# 1. Connectez-vous à votre base PostgreSQL
psql -h localhost -U postgres -d your_database

# 2. Exécutez les scripts dans l'ordre
\i sql-test-data/01-schema/create_schema.sql
\i sql-test-data/02-data/populate_data.sql
\i sql-test-data/03-performance-issues/create_performance_issues.sql
\i sql-test-data/04-security-issues/create_security_issues.sql
\i sql-test-data/05-maintenance-issues/create_maintenance_issues.sql

# 3. Testez votre agent DBA
# "Why is my database slow?" → Performance Agent
# "Audit database security" → Security Agent
# etc.

# 4. Nettoyage après tests
\i sql-test-data/99-cleanup/cleanup_all.sql
```

## 📁 Structure des Scripts

```
sql-test-data/
├── 01-schema/           # Création du schéma de base
│   └── create_schema.sql
├── 02-data/             # Population avec des données
│   ├── populate_data.sql
│   └── insert_large_datasets.sql
├── 03-performance-issues/  # Création de problèmes de performance
│   ├── create_performance_issues.sql
│   ├── missing_indexes.sql
│   └── slow_queries.sql
├── 04-security-issues/     # Création de vulnérabilités de sécurité
│   ├── create_security_issues.sql
│   ├── weak_users.sql
│   └── poor_permissions.sql
├── 05-maintenance-issues/  # Création de problèmes de maintenance
│   ├── create_maintenance_issues.sql
│   ├── bloated_tables.sql
│   └── config_issues.sql
└── 99-cleanup/            # Scripts de nettoyage
    └── cleanup_all.sql
```

## 🎲 Scénarios de Test Créés

### Performance (Agent Performance)
- Tables avec millions de lignes sans index appropriés
- Requêtes avec Cartesian products
- Sessions bloquantes et deadlocks
- Cache misses et opérations I/O intensives

### Sécurité (Agent Security)
- Utilisateurs avec privilèges excessifs
- Méthodes d'authentification faibles
- Objets publics avec données sensibles
- Politiques de sécurité au niveau ligne manquantes

### Schéma (Agent Schema)
- Tables bloatées (>20% de bloat)
- Index inutilisés et redondants
- Mauvais choix de types de données
- Contraintes de clés étrangères manquantes

### Maintenance (Agent Maintenance)
- Tables nécessitant VACUUM
- Statistiques obsolètes
- Paramètres de configuration sous-optimaux
- Croissance de base de données simulée

## ⚠️ Notes Importantes

- **Utiliser uniquement sur des bases de test** : Ces scripts créent intentionnellement des problèmes
- **Utilisation des ressources** : Les grandes datasets consommeront de l'espace disque et mémoire
- **Sauvegarde** : Considérez sauvegarder votre base avant les tests extensifs
- **Nettoyage** : Utilisez les scripts de cleanup après les tests

## 🧪 Validation

Après l'exécution des scripts, votre système PostgreSQL DBA Multi-Agent devrait pouvoir :

1. **Détecter les problèmes de performance** et suggérer des optimisations
2. **Trouver les vulnérabilités de sécurité** et recommander des corrections
3. **Analyser les problèmes de schéma** et proposer des améliorations
4. **Planifier la maintenance** et optimiser la configuration
5. **Gérer les problèmes complexes** avec une analyse coordonnée multi-domaine

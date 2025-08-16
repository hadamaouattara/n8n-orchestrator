# 🚀 n8n Orchestrator - AI/Quantum SaaS Platform

Plateforme d'orchestration n8n optimisée pour Northflank, intégrant l'IA et l'informatique quantique avec support MCP (Model Context Protocol).

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](./CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Northflank](https://img.shields.io/badge/platform-Northflank-purple.svg)](https://northflank.com)
[![n8n](https://img.shields.io/badge/powered%20by-n8n-ff6d5a.svg)](https://n8n.io)
[![Claude MCP](https://img.shields.io/badge/Claude-MCP-orange.svg)](https://anthropic.com)

## 🎯 Vision

Une plateforme unifiée qui orchestre l'intelligence artificielle et l'informatique quantique à travers des workflows automatisés, permettant à Claude d'interagir directement avec GitHub, SAP, et des backends quantiques via le protocole MCP.

```
Claude MCP ←→ GitHub ←→ n8n Orchestrator ←→ Northflank
     ↓              ↓              ↓               ↓
   Tools        Workflows      Automation      Deployment
```

## ✨ Fonctionnalités principales

### 🔗 Intégration MCP Native
- **Claude Desktop** peut exécuter directement des workflows
- **GitHub operations** via prompts en langage naturel  
- **SAP data extraction** avec transformation ML automatique
- **Quantum circuits** execution et analyse

### 🏢 Connecteur SAP Enterprise
- Extraction **OData CDS** (ACDOCA, MBEW, CKML*)
- Support **multi Company Codes** et périodes fiscales
- **Transformation ML** automatique des données
- **Audit trail** complet et governance

### ⚛️ Computing Quantique
- **Qiskit integration** avec simulateurs et IBM Quantum
- **Circuits pré-définis** : Bell states, QFT, Grover, random numbers
- **Résultats structurés** avec visualisations
- **Multi-backend** support (simulateur local, IBM, AWS Braket future)

### 📈 Production Ready
- **Multi-tenant** avec isolation RLS PostgreSQL
- **Auto-scaling** horizontal et vertical sur Northflank
- **Monitoring** Prometheus avec alertes configurées
- **Sécurité** enterprise avec RBAC et audit logging

## 🚀 Quick Start

### 1. Déploiement Northflank (5 minutes)

```bash
# 1. Créer service Northflank
# Source: GitHub Repository
# Repository: hadamaouattara/n8n-orchestrator
# Branch: main
# Port: 5678

# 2. Ajouter PostgreSQL addon
# Name: n8n-postgres
# Version: PostgreSQL 15

# 3. Configurer secrets (minimum)
export N8N_ADMIN_USER="admin"
export N8N_ADMIN_PASSWORD="SecurePassword123!"
export GITHUB_TOKEN="ghp_your_github_token"
export CLAUDE_API_KEY="sk-ant-your_claude_key"

# 4. Déployer !
# Northflank se charge du build et déploiement automatique
```

### 2. Configuration MCP Claude (2 minutes)

```json
// ~/.claude/claude_desktop_config.json
{
  "mcpServers": {
    "n8n-github": {
      "command": "curl",
      "args": [
        "-X", "POST",
        "https://your-service.northflank.app/webhook/github-mcp",
        "-H", "Content-Type: application/json",
        "-H", "X-Tenant-ID: demo-tenant",
        "-d", "@-"
      ]
    }
  }
}
```

### 3. Premier test (30 secondes)

```bash
# Test santé du service
curl https://your-service.northflank.app/healthz

# Test workflow GitHub
curl -X POST https://your-service.northflank.app/webhook/github-mcp \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: demo-tenant" \
  -d '{
    "owner": "hadamaouattara",
    "repo": "n8n-orchestrator",
    "state": "open"
  }'
```

**✅ Félicitations !** Votre plateforme est opérationnelle.

## 📚 Documentation complète

| Document | Description |
|----------|-------------|
| **[Deployment Guide](./docs/DEPLOYMENT.md)** | Guide détaillé de déploiement Northflank |
| **[API Reference](./docs/API.md)** | Documentation complète des APIs |
| **[Architecture](./docs/ARCHITECTURE.md)** | Vision architecture et patterns |
| **[Troubleshooting](./docs/TROUBLESHOOTING.md)** | Résolution de problèmes |
| **[Claude Prompts](./examples/claude-prompts.md)** | Exemples d'utilisation MCP |

---

<div align="center">

**🚀 Ready to orchestrate the future? Let's build something amazing together! 🚀**

[![Deploy on Northflank](https://img.shields.io/badge/Deploy%20on-Northflank-purple?style=for-the-badge)](https://northflank.com)
[![GitHub](https://img.shields.io/badge/Star%20on-GitHub-black?style=for-the-badge&logo=github)](https://github.com/hadamaouattara/n8n-orchestrator)
[![Discord](https://img.shields.io/badge/Join-Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/exonov)

</div>
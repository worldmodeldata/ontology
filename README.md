# Ontology Repository

This repository contains the Living Ontology System's gaming ontology definitions, rules, and related code/configuration files.

## Structure

- `ontology/` - Core ontology files (Turtle/RDF format)
  - `gaming_ontology_v1.ttl` - Main ontology definitions
  - `gaming_shapes.ttl` - SHACL shape constraints
  - `inference_rules.ttl` - OWL inference rules
  - `tenant_thresholds.ttl` - Tenant-specific thresholds
  - `shapes/` - Additional SHACL shape definitions
  - `versions/` - Version history

- `universal/` - Universal foundation ontologies
  - `human_behavior_foundation.ttl` - Universal human behavior foundation
  - `gaming_foundation_v1.ttl` - Universal gaming foundation v1.0
  - `synthesis_report.md` - Synthesis decisions documentation

- `sources/` - Source pattern extraction files
  - `unity/` - Unity Analytics patterns
  - `mixpanel/` - Mixpanel patterns
  - `gop/` - Game Ontology Project patterns
  - `production/` - Production-validated patterns

- `extensions/` - Domain extension ontologies
  - `video_playthrough_extension.ttl` - Video data integration
  - `cross_game_extension.ttl` - Cross-game integration
  - `human_behavior_extension.ttl` - Human behavior data framework

- `mappings/` - Source-to-universal mapping files
  - `unity_to_universal.ttl` - Unity to universal mappings
  - `mixpanel_to_universal.ttl` - Mixpanel to universal mappings
  - `video_to_universal.ttl` - Video to universal mappings
  - `game_source_to_universal.ttl` - Generic game source mapping framework

- `adapters/` - Data transformation adapters (Python)
  - `game_source_adapter_template.py` - Template for new adapters
  - `unity_adapter.py` - Unity Analytics adapter
  - `mixpanel_adapter.py` - Mixpanel adapter
  - `video_adapter.py` - Video data adapter

- `scripts/` - Validation and testing scripts
  - `validate_universal_coverage.py` - Coverage validation
  - `validate_extensibility.py` - Extensibility validation
  - `test_unity_adapter.py` - Unity adapter tests
  - `test_mixpanel_adapter.py` - Mixpanel adapter tests

- `adinmo/` - Adinmo-specific schema analysis and documentation

---

## Documentation

**All documentation for this ontology work is located in the `docs` repository:**

### 🎨 Visual Architecture Documentation (in `docs/09-ontology/`)
- **[ONTOLOGY_SYSTEM_VISUAL_ARCHITECTURE.md](../../docs/09-ontology/ONTOLOGY_SYSTEM_VISUAL_ARCHITECTURE.md)** - **START HERE** - Comprehensive visual guide showing:
  - High-level system architecture and component interactions
  - Detailed workflows for ontology updates, triple extraction, reasoning, and LLM integration
  - Current implementation status (Phase 0 progress)
  - Universal ontology status and file structure
  - Perfect for explaining the system to stakeholders like Tony Seale

### 📚 Primary Documentation (in `docs/09-ontology/`)
- **[UNIVERSAL_FOUNDATION_IMPLEMENTATION_SUMMARY.md](../../docs/09-ontology/UNIVERSAL_FOUNDATION_IMPLEMENTATION_SUMMARY.md)** - Implementation progress summary (Phase 0-4 complete)
- **[UNIVERSAL_FOUNDATION_CRITIQUE.md](../../docs/09-ontology/UNIVERSAL_FOUNDATION_CRITIQUE.md)** - Knowledge Graph Guys critique of the ontology work

### 📚 Quick Start Guide
- **[README_UNIVERSAL_FOUNDATION.md](README_UNIVERSAL_FOUNDATION.md)** - Quick start and usage guide (this repo)

### 📚 Implementation & Enhancement Plans (in `docs/05-implementation/`)
- **[KNOWLEDGE_GRAPH_GUYS_ENHANCEMENT_IMPLEMENTATION.md](../../docs/05-implementation/KNOWLEDGE_GRAPH_GUYS_ENHANCEMENT_IMPLEMENTATION.md)** - Comprehensive implementation plan based on Knowledge Graph Guys principles
- **[KNOWLEDGE_GRAPH_GUYS_CRITIQUE.md](../../docs/05-implementation/KNOWLEDGE_GRAPH_GUYS_CRITIQUE.md)** - Critique of implementation plan
- **[BLOG_ARTICLES_ANALYSIS.md](../../docs/05-implementation/BLOG_ARTICLES_ANALYSIS.md)** - Analysis of Knowledge Graph Guys blog articles
- **[FINAL_REVIEW_IMPLEMENTATION_PLAN.md](../../docs/05-implementation/FINAL_REVIEW_IMPLEMENTATION_PLAN.md)** - Final review of implementation plan

### 📚 Architecture Documentation (in `docs/04-architecture/`)
- **[ONTOLOGY_ARCHITECTURE.md](../../docs/04-architecture/ONTOLOGY_ARCHITECTURE.md)** - Ontology service architecture and semantic enrichment
- **[KNOWLEDGE_GRAPH_ARCHITECTURE.md](../../docs/04-architecture/KNOWLEDGE_GRAPH_ARCHITECTURE.md)** - Knowledge graph architecture (Neo4j, relationships)

### 📚 Reference Documentation (in `docs/06-reference/`)
- **[ONTOLOGY_REFERENCE.md](../../docs/06-reference/ONTOLOGY_REFERENCE.md)** - Ontology structure, classes, properties, rules reference

---

## Quick Start

See **[README_UNIVERSAL_FOUNDATION.md](README_UNIVERSAL_FOUNDATION.md)** for quick start instructions.

---

## Related Documentation

For comprehensive information about the ontology architecture, evolution, and integration:

- **🎨 Visual Architecture Guide**: `docs/09-ontology/ONTOLOGY_SYSTEM_VISUAL_ARCHITECTURE.md` - **Visual diagrams and workflows**
- **Ontology Implementation Summary**: `docs/09-ontology/UNIVERSAL_FOUNDATION_IMPLEMENTATION_SUMMARY.md`
- **Ontology Critique**: `docs/09-ontology/UNIVERSAL_FOUNDATION_CRITIQUE.md`
- **Ontology Architecture**: `docs/04-architecture/ONTOLOGY_ARCHITECTURE.md`
- **Knowledge Graph Architecture**: `docs/04-architecture/KNOWLEDGE_GRAPH_ARCHITECTURE.md`
- **Orchestrator Architecture**: `docs/04-architecture/ORCHESTRATOR_ARCHITECTURE.md`
- **Complete System Explainer**: `docs/01-system-overview/COMPLETE_SYSTEM_EXPLAINER.md`
- **Implementation Plan**: `docs/05-implementation/KNOWLEDGE_GRAPH_GUYS_ENHANCEMENT_IMPLEMENTATION.md`

---

**Last Updated:** 2025-12-27

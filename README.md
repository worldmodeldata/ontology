# Ontology Repository

This repository contains the Living Ontology System's gaming ontology definitions, rules, and related documentation.

## Structure

- `ontology/` - Core ontology files (Turtle/RDF format)
  - `gaming_ontology_v1.ttl` - Main ontology definitions
  - `gaming_shapes.ttl` - SHACL shape constraints
  - `inference_rules.ttl` - OWL inference rules
  - `tenant_thresholds.ttl` - Tenant-specific thresholds
  - `shapes/` - Additional SHACL shape definitions
  - `versions/` - Version history

- `adinmo/` - Adinmo-specific schema analysis and documentation

## Ontology TODO

### High Priority

1. **Automatic Ontology Evolution Pipeline**
   - Design of an automatic ontology evolution pipeline that connects schema analysis to ontology suggestions
   - The system should enable a human to go through ontology suggestions in a list and add their human input and research to it
   - This can then be stored in our ontology
   - **Status:** Design phase
   - **Related Documentation:** 
     - `docs/04-architecture/ONTOLOGY_ARCHITECTURE.md` (Part 7: Ontology Evolution and Schema Discovery)
     - `docs/04-architecture/ORCHESTRATOR_ARCHITECTURE.md` (Section 4.5.4c: Schema Evolution and Ontology Discovery)

---

## Related Documentation

For comprehensive information about the ontology architecture, evolution, and integration:

- **Ontology Architecture:** `docs/04-architecture/ONTOLOGY_ARCHITECTURE.md`
- **Orchestrator Architecture:** `docs/04-architecture/ORCHESTRATOR_ARCHITECTURE.md`
- **Complete System Explainer:** `docs/01-system-overview/COMPLETE_SYSTEM_EXPLAINER.md`

---

**Last Updated:** 2025-12-02


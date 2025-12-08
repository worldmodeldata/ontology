# Production Ontology Patterns Documentation

**Author:** Gi Fernando  
**Date:** 2025-12-27  
**Status:** Active Documentation  
**Purpose:** Document validated patterns from current production ontology (`gaming_ontology_v1.ttl`)

---

## Overview

This document catalogs production-validated patterns from our current gaming ontology that have been tested and proven in production with real tenant data (Flick, Avakin, Adinmo).

---

## 1. Core Entity Classes

### 1.1 Top-Level Hierarchy

**Pattern:** Four-level class hierarchy with clear separation of concerns

```
Entity (top-level)
├── Actor (entities that perform actions)
│   └── Device (gaming-specific actors)
├── Event (temporal occurrences)
│   ├── Session
│   │   └── GameSession
│   ├── AdEvent
│   │   ├── Bid
│   │   ├── Impression
│   │   └── AdInteraction
│   └── Transaction
│       └── InAppPurchase
└── Resource (consumable resources)
```

**Production Validation:**
- Used in cross-tenant queries across Flick, Avakin, Adinmo
- Validated in Neo4j knowledge graph aggregation
- Proven in feature engineering for JEPA training

**Key Insight:** The Device → Session → Event hierarchy enables both individual event analysis and aggregated behavioral analysis.

### 1.2 Device/Player Pattern

**Pattern:** `Device` class with `altLabel` for "Player" and "User"

```turtle
:Device a owl:Class ;
    rdfs:subClassOf :Actor ;
    rdfs:label "Device"@en ;
    skos:altLabel "Player"@en, "User"@en ;
    rdfs:comment "Represents the same concept as Player or User in different games" .
```

**Production Validation:**
- Successfully unifies different tenant terminology
- Flick uses "Player", Adinmo uses "Device", all map to same class
- Cross-tenant queries work seamlessly

**Key Insight:** Using `altLabel` for semantic aliasing enables terminology flexibility while maintaining ontological consistency.

---

## 2. Behavioral Classification Patterns

### 2.1 Engagement Level Pattern

**Pattern:** Three-level engagement hierarchy with disjoint classes

```turtle
:EngagementLevel a owl:Class ;
    rdfs:subClassOf :Entity .

:LowEngagement a owl:Class ;
    rdfs:subClassOf :EngagementLevel ;
    skos:definition "User with low engagement (1-2 sessions)" .

:MediumEngagement a owl:Class ;
    rdfs:subClassOf :EngagementLevel ;
    skos:definition "User with medium engagement (3-9 sessions)" .

:HighEngagement a owl:Class ;
    rdfs:subClassOf :EngagementLevel ;
    skos:definition "User with high engagement (10+ sessions)" .
```

**Production Validation:**
- Thresholds validated across all tenants (Flick: session-based, Avakin: session-based, Adinmo: session-based)
- Used in enrichment rules for semantic classification
- Proven valuable for retention prediction models

**Key Insight:** Session count is a universal engagement metric that works across all game types.

### 2.2 Monetization Segment Pattern

**Pattern:** Four-segment monetization hierarchy (NonPayer, Minnow, Dolphin, Whale)

```turtle
:MonetizationSegment a owl:Class ;
    rdfs:subClassOf :Entity .

:NonPayer a owl:Class ;
    rdfs:subClassOf :MonetizationSegment ;
    skos:definition "User who has never made a purchase" .

:Minnow a owl:Class ;
    rdfs:subClassOf :MonetizationSegment ;
    skos:definition "User with low spending (£0-£10)" .

:Dolphin a owl:Class ;
    rdfs:subClassOf :MonetizationSegment ;
    skos:definition "User with medium spending (£10-£50)" .

:Whale a owl:Class ;
    rdfs:subClassOf :MonetizationSegment ;
    skos:definition "User with high spending (£50+)" .
```

**Production Validation:**
- Tenant-specific thresholds configured via `MonetizationThresholds` class
- Flick: 425 IAPs = Whale threshold (validated)
- Avakin: 34,190 IAPs = Whale threshold (validated)
- Adinmo: 1,680 IAPs = Whale threshold (validated)
- Used in enrichment rules for semantic segmentation

**Key Insight:** IAP count is more reliable than monetary value for cross-tenant monetization segmentation due to currency and pricing differences.

### 2.3 Retention Status Pattern

**Pattern:** Three-state retention classification (Churned, AtRisk, Retained)

```turtle
:RetentionStatus a owl:Class ;
    rdfs:subClassOf :Entity .

:Churned a owl:Class ;
    rdfs:subClassOf :RetentionStatus ;
    skos:definition "User who has not returned after first session" .

:AtRisk a owl:Class ;
    rdfs:subClassOf :RetentionStatus ;
    skos:definition "User who may churn soon" .

:Retained a owl:Class ;
    rdfs:subClassOf :RetentionStatus ;
    skos:definition "User who continues to engage regularly" .
```

**Production Validation:**
- Used in retention prediction models
- Validated across all tenants for churn prediction accuracy
- Critical for LTV prediction

**Key Insight:** Binary retained/churned classification is too simplistic; AtRisk category enables proactive intervention.

---

## 3. Relationship Patterns

### 3.1 Device-Session-Event Hierarchy

**Pattern:** Hierarchical relationships with inverse properties

```turtle
:hasSession a owl:ObjectProperty ;
    rdfs:domain :Device ;
    rdfs:range :Session ;
    owl:inverseOf :belongsToDevice .

:belongsToDevice a owl:ObjectProperty ;
    rdfs:domain :Session ;
    rdfs:range :Device .
```

**Production Validation:**
- Enables efficient graph traversal in Neo4j
- Used in cross-tenant queries: "Find all sessions for devices with high engagement"
- Validated in knowledge graph aggregation queries

**Key Insight:** Defining inverse properties explicitly improves query performance and semantic clarity.

### 3.2 Cross-Entity Relationships

**Pattern:** Multiple relationship types connecting entities

```turtle
:occursInGame a owl:ObjectProperty ;
    rdfs:domain :Session ;
    rdfs:range :Game .

:playsGame a owl:ObjectProperty ;
    rdfs:domain :Device ;
    rdfs:range :Game ;
    rdfs:comment "Inferred from hasSession and occursInGame" .

:hasInAppPurchase a owl:ObjectProperty ;
    rdfs:domain :Session ;
    rdfs:range :InAppPurchase .
```

**Production Validation:**
- Enables complex multi-hop queries
- Used in feature engineering: "Devices that play Game X and have made purchases"
- Validated in cross-tenant analytics

**Key Insight:** Relationship patterns enable graph-based feature engineering that traditional relational models cannot support.

---

## 4. Tenant Alignment Patterns

### 4.1 Tenant-Specific Threshold Configuration

**Pattern:** Configuration class for tenant-specific thresholds

```turtle
:MonetizationThresholds a owl:Class ;
    rdfs:subClassOf :Entity .

:appliesToTenant a owl:DatatypeProperty ;
    rdfs:domain :MonetizationThresholds ;
    rdfs:range xsd:string .

:whaleIapThreshold a owl:DatatypeProperty ;
    rdfs:domain :MonetizationThresholds ;
    rdfs:range xsd:integer .
```

**Production Validation:**
- Used to configure different thresholds per tenant
- Flick, Avakin, Adinmo all have different IAP count distributions
- Enables unified ontology with tenant-specific semantics

**Key Insight:** Configuration pattern enables ontology reuse while preserving tenant-specific business logic.

### 4.2 Cross-Tenant Query Patterns

**Pattern:** Queries that work across all tenants using unified ontology

**Example Query:** "Find all devices with high engagement across all games"

```cypher
MATCH (d:Device)-[:hasEngagementLevel]->(e:HighEngagement)
RETURN d.deviceId, COUNT(DISTINCT d) as high_engagement_count
```

**Production Validation:**
- Successfully executed across Flick, Avakin, Adinmo
- Enables portfolio-level analytics
- Validated in knowledge graph aggregation

**Key Insight:** Unified ontology enables cross-tenant analytics that would be impossible with separate schemas.

---

## 5. Data Property Patterns

### 5.1 Identifier Properties

**Pattern:** Functional properties for unique identifiers

```turtle
:deviceId a owl:DatatypeProperty , owl:FunctionalProperty ;
    rdfs:domain :Device ;
    rdfs:range xsd:string .

:sessionId a owl:DatatypeProperty , owl:FunctionalProperty ;
    rdfs:domain :Session ;
    rdfs:range xsd:string .
```

**Production Validation:**
- Enables efficient lookup and deduplication
- Validated in data pipeline deduplication logic
- Critical for cross-tenant data consistency

**Key Insight:** Marking identifier properties as `FunctionalProperty` enforces uniqueness constraints at the ontological level.

### 5.2 Temporal Properties

**Pattern:** Timestamp properties for temporal analysis

```turtle
:activityTimestamp a owl:DatatypeProperty ;
    rdfs:domain :Event ;
    rdfs:range xsd:dateTime .
```

**Production Validation:**
- Used in temporal sequence construction for JEPA training
- Enables session duration calculation
- Validated in time-series feature engineering

**Key Insight:** Temporal properties enable temporal pattern recognition and sequence modeling.

### 5.3 Behavioral Properties

**Pattern:** Aggregated behavioral metrics

```turtle
:sessionCount a owl:DatatypeProperty ;
    rdfs:domain :Device ;
    rdfs:range xsd:integer .

:totalSpent a owl:DatatypeProperty ;
    rdfs:domain :Device ;
    rdfs:range xsd:decimal .
```

**Production Validation:**
- Used in enrichment rules for engagement/retention classification
- Aggregated in Neo4j knowledge graph
- Validated in feature engineering for ML models

**Key Insight:** Pre-aggregated properties enable efficient querying but must be kept consistent with source data.

---

## 6. Enrichment Rules Patterns

### 6.1 Engagement Classification Rule

**Pattern:** Rule-based engagement classification

**Logic:**
- `sessionCount <= 2` → `LowEngagement`
- `3 <= sessionCount <= 9` → `MediumEngagement`
- `sessionCount >= 10` → `HighEngagement`

**Production Validation:**
- Applied in `enrich_with_ontology.py`
- Validated against manual classification
- Used in cross-tenant analytics

### 6.2 Monetization Classification Rule

**Pattern:** Rule-based monetization classification with tenant-specific thresholds

**Logic:**
- Load tenant-specific thresholds from `MonetizationThresholds`
- Classify based on `total_iaps` or `totalSpent`
- Apply tenant-specific thresholds

**Production Validation:**
- Applied in `enrich_with_ontology.py`
- Validated with Flick (425 IAPs = Whale), Avakin (34,190 IAPs = Whale), Adinmo (1,680 IAPs = Whale)
- Critical for monetization segmentation

---

## 7. Patterns to Preserve

### 7.1 Hierarchical Class Structure
- **Why:** Enables efficient graph traversal and inheritance reasoning
- **Preserve:** Four-level hierarchy (Entity → Actor/Event/Resource → Specific classes)

### 7.2 Behavioral Classification
- **Why:** Proven valuable for ML feature engineering
- **Preserve:** Engagement, Monetization, Retention classification patterns

### 7.3 Tenant-Specific Configuration
- **Why:** Enables ontology reuse with tenant-specific semantics
- **Preserve:** Configuration class pattern for thresholds

### 7.4 Relationship Patterns
- **Why:** Enables complex graph queries
- **Preserve:** Inverse properties, hierarchical relationships

---

## 8. Gaps to Fill

### 8.1 Missing Universal Patterns
- **Gap:** No universal "HumanActor" or "Activity" abstraction
- **Impact:** Cannot easily extend to non-gaming domains
- **Recommendation:** Create universal foundation layer

### 8.2 Limited Event Types
- **Gap:** Only gaming-specific events defined
- **Impact:** Cannot represent general behavioral events
- **Recommendation:** Add universal event types

### 8.3 No Cross-Game Patterns
- **Gap:** No explicit cross-game player relationships
- **Impact:** Cannot analyze multi-game player behavior
- **Recommendation:** Add cross-game extension

### 8.4 No Multi-Modal Support
- **Gap:** No video, sensor, or questionnaire data support
- **Impact:** Cannot integrate multi-modal behavioral data
- **Recommendation:** Add multi-modal extensions

---

## 9. Lessons Learned

### 9.1 Ontology-First Design Works
- **Lesson:** Starting with ontology before schema design enables cross-tenant alignment
- **Evidence:** Successful cross-tenant queries with unified ontology

### 9.2 Tenant Configuration is Critical
- **Lesson:** Different tenants need different thresholds, but same structure
- **Evidence:** Tenant-specific thresholds enable unified ontology with different semantics

### 9.3 Behavioral Classification is Valuable
- **Lesson:** Semantic classification enables ML feature engineering
- **Evidence:** Engagement/Retention/Monetization classifications used in all ML models

### 9.4 Graph Relationships Enable Complex Analysis
- **Lesson:** Graph structure enables queries impossible in relational models
- **Evidence:** Cross-tenant analytics and feature engineering using graph traversal

---

## 10. Integration Points

### 10.1 Data Pipeline Integration
- **File:** `data-platform/assets/ontology_assets.py`
- **Pattern:** Load ontology rules as Dagster assets
- **Usage:** Semantic enrichment during data processing

### 10.2 Knowledge Graph Integration
- **File:** `data-platform/assets/gi_agent_assets.py`
- **Pattern:** Aggregate enriched data into Neo4j
- **Usage:** Graph-based analytics and feature engineering

### 10.3 Feature Engineering Integration
- **File:** `product-provider-portal/backend/services/feature_engineer.py`
- **Pattern:** Compute graph-based features using ontology relationships
- **Usage:** ML feature generation for JEPA training

---

## 11. References

- **Production Ontology:** `ontology/gaming_ontology_v1.ttl`
- **Enrichment Implementation:** `data-platform/sdk/operations/enrich/enrich_with_ontology.py`
- **Knowledge Graph Architecture:** `docs/04-architecture/KNOWLEDGE_GRAPH_ARCHITECTURE.md`
- **Ontology Architecture:** `docs/04-architecture/ONTOLOGY_ARCHITECTURE.md`


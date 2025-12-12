# Adinmo Source Patterns – Extraction Report

**Source**: Adinmo in‑game advertising telemetry (Snowflake exports)  
**Inputs in this repo**: `adinmo/schema_*.yaml`  
**Purpose**: Define a *source vocabulary* (`sources/adinmo`) that can be mapped into the WorldModelData universal gaming ontology (`ug:` / `ub:`).

## What Adinmo adds beyond Unity/Mixpanel

Adinmo is not just “game analytics”; it is a **full ad‑monetization + attribution funnel**:

- **Bid request → impression → tracker events (render/view/click/video quartiles) → attributed install → post‑install session → IAP**
- Rich ad‑tech concepts:
  - **Placement** (`PLACEMENT_KEY`, `PLACEMENT_NAME`, sizes, fit)
  - **Creative / asset** (`CREATIVE_ID`, `IMAGE_GUID`)
  - **Exchange / demand** (`AD_EXCHANGE`, seat/protocols where present)
  - **Viewability / validity** (`valid_impression`, `invalid_impression`, `IS_MEASURED`, coverage arrays)
  - **Revenue** (`ACTUAL_REVENUE`, bid price)
  - **Engagement quality** (`DWELL_TIME`, `PLAYER_ENGAGEMENT_SCORE`, `SESSION_TIME_MS`)

## Canonical “golden thread” identifiers (from schemas)

- **ANON_DEVICE_ID**: cross-table user identity (privacy-preserving)
- **SESSION_ID**: joins sessions ↔ bids ↔ impressions ↔ tracker events
- **BID_ID**: joins bids ↔ impressions ↔ tracker events
- **IMPRESSION_ID**: joins impressions ↔ tracker events
- **CAMPAIGN_ID / IMAGE_GUID**: joins to campaign/creative reporting and installs

## Output artifacts

- **Source pattern ontology**: `sources/adinmo/adinmo_patterns.ttl`
- **Mapping (OWL) to universal**: `mappings/adinmo_to_universal.ttl`
- (Optional) **Adapter**: `adapters/adinmo_adapter.py` (row → universal event dicts)

## Notes / open questions (to carry as business semantics)

The schemas include valuable “critical questions” (e.g., `REQUEST_ID` vs `SDK_REQUEST_ID`, `IMP_ID` vs `IMPRESSION_ID`, how session_end is tracked). These should become:

- **Business semantics annotations** on the relevant universal properties/classes (preferred), and/or
- A dedicated “data quality / provenance” extension (future).



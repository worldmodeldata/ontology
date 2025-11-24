# Adinmo Data Schema Documentation

**Project**: Adinmo In-Game Advertising Dataset Analysis  
**Purpose**: Comprehensive data cataloging, relationship mapping, and commercial opportunity analysis  
**Date**: November 24, 2025  
**Status**: ✅ Complete

---

## 📁 Documentation Structure

### Core Schema Files
- **`schema_bids.yaml`** - Ad bid requests (68 fields)
- **`schema_impressions.yaml`** - Ad impressions shown (87 fields) 
- **`schema_iap.yaml`** - In-app purchases (44 fields)
- **`schema_sessions.yaml`** - Gaming sessions (48 fields)
- **`schema_tracker_events.yaml`** - User interactions with ads (54 fields)
- **`schema_attributed_installs.yaml`** - App installs from ads (13 fields)

### Supporting Documentation
- **`EXECUTIVE_SUMMARY.md`** - 📊 Strategic overview and recommendations (START HERE)
- **`data_relationships.md`** - 🔗 Entity relationships, joins, SQL examples
- **`industry_use_cases.md`** - 💰 Revenue opportunities and buyer profiles
- **`critical_questions.md`** - ❓ 50+ questions requiring clarification
- **`data_analysis.json`** - 📈 Statistical analysis of sample data

### Analysis Scripts
- **`analyze_data.py`** - Python script for data profiling

---

## 🚀 Quick Start

### For Executives
**Read First**: `EXECUTIVE_SUMMARY.md`
- Dataset overview and business value
- Revenue projections ($5M-$25M annually)
- Go-to-market strategy
- Critical next steps

### For Product Managers
**Read**: `industry_use_cases.md`
- 8 buyer verticals with specific use cases
- Pricing strategies ($10K - $1M per buyer)
- Competitive positioning
- Sales playbooks

### For Data Scientists
**Read**: Individual `schema_*.yaml` files + `data_relationships.md`
- Complete field definitions with docstrings
- Data types, nullable status, cardinality
- Join patterns and SQL examples
- ML training opportunities

### For Legal/Compliance
**Read**: `critical_questions.md` (Priority 7)
- Privacy and data sharing permissions
- GDPR/CCPA compliance strategy
- PII handling requirements

---

## 🎯 Key Findings

### Dataset Characteristics
- **6 tables** capturing complete user journeys
- **TBs of data** (estimated 32-323 GB/day production scale)
- **Longitudinal tracking** via ANON_DEVICE_ID across all tables
- **Complete attribution chain**: Ad exposure → Click → Install → Purchase

### Unique Value Propositions
1. **Longitudinal behavioral data** - Track users across multiple sessions
2. **Cross-game visibility** - See behavior across game portfolio
3. **Dual monetization streams** - Both ad revenue AND in-app purchases
4. **Failure data** - 95% of IAP attempts fail (rare to capture failures)
5. **Attribution completeness** - Full chain from ad to revenue

### Critical Insights
1. **Massive IAP failure rate** (95%+) = conversion optimization opportunity
2. **Privacy-first design** - Many demographic fields null by default
3. **Energy industry opportunity** - Gaming patterns predict electricity demand
4. **ML training dataset** - Sequential behavioral data ideal for AI models

---

## 💰 Revenue Opportunity Summary

### Tier 1: AI/ML Training ($200K-$1M per buyer)
- OpenAI, Anthropic, Google, Meta
- Sequence modeling, causal inference, fraud detection
- **Target**: 5-10 buyers globally

### Tier 2: Energy & Infrastructure ($100K-$500K per buyer)
- Utility companies, grid operators
- Electricity demand forecasting from gaming patterns
- **Target**: 10-20 buyers

### Tier 3: AdTech & Gaming ($30K-$200K per buyer)
- Ad exchanges, game publishers, MMPs
- Benchmarking, competitive intelligence
- **Target**: 50-100 buyers

### Tier 4: Financial Services ($50K-$300K per buyer)
- Banks, credit cards, fintech
- Spending behavior, credit risk modeling
- **Target**: 20-30 buyers

**Total Revenue Potential**: $5M-$25M annually at scale

---

## 📊 Data Model Overview

### The Golden Thread: ANON_DEVICE_ID
**ANON_DEVICE_ID** appears in ALL 6 tables and enables:
- User journey reconstruction across sessions
- Cross-game behavioral analysis
- Attribution from ad exposure to revenue
- Privacy-preserving user tracking

### Entity Relationships
```
sessions (1) ──→ (N) bids
bids (1) ──→ (N) impressions
impressions (1) ──→ (N) tracker_events
tracker_events (click) ──→ (1) attributed_installs
sessions (1) ──→ (N) iap
```

**See `data_relationships.md` for detailed ER diagrams and SQL examples**

---

## ❓ Critical Questions (Must Answer Before Sales)

### Priority 1: Data Integrity
1. Is ANON_DEVICE_ID global or per-game?
2. How are session ends tracked?
3. What attribution window is used?
4. Revenue calculation formula?

### Priority 2: Field Definitions
5. REQUEST_ID vs SDK_REQUEST_ID?
6. IMP_ID vs IMPRESSION_ID?
7. Dynamic pricing algorithm?
8. Player engagement score formula?
9. What is "magnified" event?

**See `critical_questions.md` for complete list (50+ questions with priorities)**

---

## 📋 Schema Field Statistics

| Table | Total Fields | Core Identity | Device Info | Privacy/Consent | Revenue/Business |
|-------|--------------|---------------|-------------|-----------------|------------------|
| sessions | 48 | 4 | 10 | 13 | 5 |
| bids | 68 | 5 | 11 | 10 | 15 |
| impressions | 87 | 11 | 11 | 10 | 8 |
| tracker_events | 54 | 7 | 10 | 6 | 5 |
| iap | 44 | 4 | 10 | 9 | 8 |
| attributed_installs | 13 | 6 | 0 | 0 | 4 |

**Total unique fields across all tables**: 200+ (with overlap)

---

## 🔍 Notable Data Quality Issues

### Always Null Fields (100% null)
- Geographic: `LAT`, `LONG` (privacy restriction?)
- Demographic: `AGE`, `SEX`, `USER_EMAIL` (never collected)
- Technical: `PIXALATE_*` scores (integration ended)
- Business: `CONSENT_CCPA` (not implemented?)

### High Null Rate (>90%)
- `CONSENT_GDPR` (91-94% null)
- `CONSENT_PERSONALISED_GDPR` (93% null)
- `VIDEO_DURATION_MS` (83% null - most ads are banners)

### Interesting Distributions
- `IAP_PURCHASE_MADE`: 95%+ false (massive failure rate!)
- `TRACKING_ENABLED`: 100% false (iOS ATT impact?)
- `FAILURE_REASON`: 95%+ "UserCancelled" (why so high?)

**Action Required**: Investigate these patterns with Adinmo team

---

## 🔄 Data Lineage & Processing

### Current State
1. **Source**: Adinmo's Snowflake database (read-only access)
2. **Sample**: 24 hours (Sept 15, 2025), ~1000 rows per table
3. **Format**: CSV exports from Snowflake

### Proposed Pipeline (from Analysis Document)
1. **Ingest**: Pull from Adinmo Snowflake (scheduled queries / data sharing)
2. **Store**: Your Snowflake instance OR S3/Azure (Parquet format)
3. **Transform**: Multi-format exports (Raw, OTLP, JEPA, Aggregated)
4. **Deliver**: S3 access, SFTP, API to buyers

**See full architecture in `Adinmo In-Game Advertising Platform_ Data Volume Analysis, Compression, and Batch Export Ideas.txt`**

---

## 🏭 Industry Applications

### AI/ML Training
- Sequence models (LSTMs, Transformers)
- Reinforcement learning
- Fraud detection
- Propensity modeling
- Causal inference

### Energy & Infrastructure
- Electricity demand forecasting
- Grid capacity planning
- Load balancing
- 5G rollout strategy

### Financial Services
- Credit risk modeling
- Spending behavior analysis
- Payment friction optimization
- Fraud detection

### Telecommunications
- Network capacity planning
- QoS optimization
- Device adoption forecasting

### AdTech & Gaming
- Benchmarking (CPM, fill rate, CTR)
- Creative optimization
- Attribution validation
- Competitive intelligence

**See `industry_use_cases.md` for detailed use case playbooks**

---

## 📝 Next Steps Checklist

### ✅ Completed
- [x] Data cataloging (6 tables, 300+ fields documented)
- [x] Relationship mapping (ER diagrams, SQL examples)
- [x] Industry use case identification (8 verticals)
- [x] Commercial opportunity sizing ($5M-$25M potential)
- [x] Question cataloging (50+ questions prioritized)

### 🔄 In Progress
- [ ] Answer Priority 1-2 questions with Adinmo team
- [ ] Legal review (data sharing permissions)
- [ ] Technical validation (SQL integrity checks)
- [ ] Sample dataset preparation for prospects

### 📅 Upcoming (Week 1)
- [ ] Schedule call with Adinmo (Yavuz)
- [ ] Document formal answers to critical questions
- [ ] Legal counsel consultation
- [ ] Update schemas with confirmed information

### 📅 Upcoming (Weeks 2-4)
- [ ] Product definition (tiered offerings)
- [ ] Pricing matrix
- [ ] Pilot customer recruitment (5 targets)
- [ ] Data delivery infrastructure
- [ ] Buyer portal & documentation

---

## 👥 Stakeholders & Contacts

### Primary Contacts
- **Adinmo**: Yavuz Acikalin
- **WMD Team**: Gi Fernando, Richard, Allan, Rhea, Loucas

### Key Discussion Topics for Next Call
1. Confirm ANON_DEVICE_ID scope (global vs per-game)
2. Clarify session end tracking
3. Attribution window details
4. Data sharing permissions review
5. Historical data availability (6+ months?)

---

## 📚 Additional Resources

### External References
- IAB Content Taxonomy: https://www.iab.com/guidelines/content-taxonomy/
- MRC Viewability Standards: https://www.mediaratingcouncil.org/
- Snowflake Best Practices: https://docs.snowflake.com/
- GDPR Guidelines: https://gdpr.eu/

### Internal Documents
- Original notes: `pm/Notes - Data journey walk through.txt`
- Volume analysis: `pm/Adinmo In-Game Advertising Platform_ Data Volume Analysis...txt`
- Sample data: `data-models/seeds/adinmo/*.csv`

---

## 🆘 Getting Help

### For Questions About
- **Schema definitions**: See individual `schema_*.yaml` files
- **Relationships & joins**: See `data_relationships.md`
- **Business strategy**: See `EXECUTIVE_SUMMARY.md`
- **Buyer use cases**: See `industry_use_cases.md`
- **Data quality**: See `critical_questions.md`

### Contact
- **Project Lead**: Gi Fernando
- **Documentation**: AI Analysis (this package)
- **Technical Questions**: Review with data engineering team

---

## 📄 Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-24 | AI Analyst | Initial comprehensive analysis |
| | | | - 6 schema files created |
| | | | - 5 supporting docs created |
| | | | - 50+ questions cataloged |
| | | | - Revenue opportunity sized |

---

## 🎓 Key Learnings & Best Practices

### What Makes This Dataset Valuable
1. **Longitudinal** - Not snapshots, but user journeys over time
2. **Complete** - Entire funnel from ad to revenue captured
3. **Rich** - 87 fields in impressions table alone
4. **Scale** - TBs of data, millions of users
5. **Privacy-compliant** - Anonymized by design

### What Makes It Challenging
1. **Complexity** - 6 tables, 200+ fields, complex joins
2. **Ambiguity** - 50+ fields need clarification
3. **Privacy** - Many fields null due to privacy restrictions
4. **Quality** - Some integration issues (Pixalate ended)

### How to Maximize Value
1. **Position as ML training data** - Highest willingness-to-pay
2. **Target non-obvious buyers** - Energy, finance (less competition)
3. **Emphasize uniqueness** - Longitudinal, cross-game, attribution chain
4. **Start with pilots** - Validate use cases before scaling
5. **Build recurring revenue** - Annual subscriptions, not one-time

---

## 🏆 Success Criteria

This analysis is successful if it enables:

1. ✅ **Complete understanding** of dataset structure and relationships
2. ✅ **Clear articulation** of commercial value proposition
3. ✅ **Identification** of high-value buyer segments
4. ✅ **Prioritization** of critical questions to answer
5. ✅ **Actionable roadmap** for go-to-market strategy

**Next Milestone**: Convert first pilot customer (prove commercial viability)

---

**For questions or clarifications, refer to individual documentation files or contact the project team.**

**Start with `EXECUTIVE_SUMMARY.md` for strategic overview, then dive into specific docs as needed.**


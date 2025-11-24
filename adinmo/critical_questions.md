# Adinmo Data: Critical Questions & Areas of Uncertainty

## Overview
This document catalogs all uncertain, unclear, or ambiguous aspects of the Adinmo dataset that require clarification from the data provider (Yavuz/Adinmo team). Questions are organized by priority and category.

---

## Priority 1: CRITICAL - Data Integrity & Business Logic

### Q1.1: ANON_DEVICE_ID Scope
**Question**: Is `ANON_DEVICE_ID` unique per device globally, or unique per device PER GAME?

**Why Critical**: This fundamentally changes how we can link data across games.

**Impact**:
- **If per-device globally**: Can track users across all games (portfolio-level insights)
- **If per-device-per-game**: Cannot link same user across games (siloed analysis)

**Evidence**: Notes mention "per user / per game" but this needs confirmation.

**Follow-up**: If per-device-per-game, is there ANY way to link users across games?

---

### Q1.2: Session End Tracking
**Question**: How are session ends tracked? Is there a `session_end` event type, or is it inferred?

**Why Critical**: Session duration is a key metric but we only see `session_start` events.

**Impact**:
- Cannot calculate session duration without end time
- Cannot identify session timeouts vs explicit closes
- Affects engagement metrics significantly

**Possible Answers**:
- Separate `session_end` event (where?)
- Inferred from next session start
- Timeout-based (what's the timeout?)
- Tracked elsewhere (different table?)

---

### Q1.3: Attribution Window
**Question**: What attribution window is used for `attributed_installs`?

**Why Critical**: Determines which clicks/impressions get credit for installs.

**Typical Windows**: 1-day, 7-day, 30-day

**Impact**:
- 1-day window = very conservative (miss delayed installs)
- 30-day window = generous (may over-attribute)
- Affects campaign ROI calculations dramatically

**Related**: Are there different windows for different campaigns?

---

### Q1.4: Revenue Reconciliation
**Question**: In `impressions` table, what's the relationship between `BID_PRICE` and `ACTUAL_REVENUE`?

**Why Critical**: Need to understand how revenue is calculated for billing.

**Observed**: 
- `BID_PRICE` is CPM (cost per 1000 impressions)
- `ACTUAL_REVENUE` is often 0 (for invalid impressions)

**Formula Needed**:
```
ACTUAL_REVENUE = f(BID_PRICE, EVENT_TYPE, ???)

If EVENT_TYPE = 'valid_impression':
  ACTUAL_REVENUE = BID_PRICE / 1000  ???
  
If EVENT_TYPE = 'invalid_impression':
  ACTUAL_REVENUE = 0  ???
```

**Follow-up**: Are there any revenue share splits or fees deducted?

---

## Priority 2: HIGH - Field Definitions & Business Logic

### Q2.1: Request ID vs SDK Request ID
**Question**: What's the difference between `REQUEST_ID` and `SDK_REQUEST_ID`?

**Tables**: Both appear in `bids` table

**Why Important**: Redundant fields suggest different systems/versions.

**Hypotheses**:
- Different SDK versions use different ID schemes?
- Batch requests have SDK_REQUEST_ID, individual have REQUEST_ID?
- One is client-side, one is server-side?

---

### Q2.2: IMP_ID vs IMPRESSION_ID  
**Question**: What's the difference between `IMP_ID` and `IMPRESSION_ID`?

**Tables**: 
- `IMPRESSION_ID` in impressions table (primary)
- `IMP_ID` in bids table and tracker_events table

**Why Important**: May represent different stages of impression lifecycle.

**Hypotheses**:
- `IMP_ID` = requested impression ID
- `IMPRESSION_ID` = actual delivered impression ID
- They're the same for successful impressions?

---

### Q2.3: Dynamic Pricing Algorithm
**Question**: How does `USED_DYNAMIC_PRICING` actually work?

**Table**: `bids`

**Why Important**: Dynamic pricing is revenue-critical.

**What We Need**:
- What factors determine floor price adjustments?
- How much does price vary? (± 10%? ± 50%?)
- Is it per-user, per-game, per-placement, per-time?
- What's the machine learning model (if any)?

---

### Q2.4: Player Engagement Score Calculation
**Question**: How is `PLAYER_ENGAGEMENT_SCORE` calculated?

**Table**: `impressions`

**Why Important**: Used for optimization and quality scoring.

**Inputs (guesses)**:
- Dwell time?
- Session depth?
- Historical engagement?
- Game context?

**Range**: 0-100? 0-1? Unbounded?

---

### Q2.5: "Magnified" Event
**Question**: What exactly triggers a `magnified` tracker event?

**Table**: `tracker_events`

**Why Important**: This appears unique to in-game advertising.

**Context**: Notes mention "magnified" is unique to in-game ads.

**Details Needed**:
- Is this a zoom/expand gesture?
- Is it automatic or user-initiated?
- What percentage of impressions get magnified?
- Does it indicate higher engagement?

---

## Priority 3: MEDIUM - Data Quality & Null Fields

### Q3.1: Always-Null Geographic Fields
**Question**: Why are `LAT` and `LONG` always null (100% null rate)?

**Tables**: All tables with geo fields

**Hypotheses**:
- Privacy policy restriction?
- Not implemented yet?
- Consent-gated (requires specific permission)?
- Technical limitation (GPS not available)?

**Impact**: Cannot do precise geo-targeting or analysis.

**Related**: Would IP-based geolocation be available instead?

---

### Q3.2: Always-Null Demographic Fields
**Question**: Why are `AGE`, `SEX`, `USER_EMAIL` always null?

**Tables**: `impressions`, `sessions`

**Hypotheses**:
- Never collected (privacy-by-design)?
- Requires explicit consent (never given)?
- Feature not implemented?

**Impact**: Cannot do demographic segmentation.

**Related**: Are there alternative demographic signals?

---

### Q3.3: TRACKING_ENABLED Always False
**Question**: Why is `TRACKING_ENABLED` always false in sessions table?

**Hypotheses**:
- iOS ATT (App Tracking Transparency) impact - everyone opted out?
- Field broken (per notes: "might be broken")?
- Misinterpreted field meaning?

**Impact**: If truly broken, can we ignore it? If accurate, major attribution implications.

**iOS ATT Context**: Since iOS 14.5 (April 2021), ATT requires permission for IDFA access.

---

### Q3.4: CONSENT_CCPA Always Null
**Question**: Why is `CONSENT_CCPA` always null (100%) in most tables?

**Hypotheses**:
- Feature not implemented yet?
- Only applies to California users (rare in sample)?
- Different field name used?

**Impact**: Cannot verify CCPA compliance if needed.

---

### Q3.5: Pixalate Fields
**Question**: What happened to Pixalate integration?

**Context**: Notes mention "stopped pixalate_ip_fraud (losing money so finished partnership)"

**Details Needed**:
- When did partnership end?
- Is there replacement fraud detection?
- Should we ignore these fields entirely?
- Are there other fraud signals we should use instead?

---

## Priority 4: MEDIUM - Business Context

### Q4.1: No-Bid Reasons
**Question**: What specifically causes each `NO_BID_REASON`?

**Table**: `bids`

**Observed Values**:
- "No Content"
- "No Fill"
- "Timeout"

**Need**: Detailed explanation of each and how to reduce them.

**Business Impact**: No-bids = lost revenue opportunity.

---

### Q4.2: IAP Failure Reasons
**Question**: What causes each `FAILURE_REASON` in IAP table?

**Observed Values**:
- "UserCancelled" (95%+ of failures)
- "PaymentDeclined"
- "InsufficientFunds"
- "NetworkError"
- "InvalidProduct"

**Critical**: "UserCancelled" is 95%+ - why so high?

**Details Needed**:
- At what stage do users cancel?
- Is price too high?
- Is UX confusing?
- Are payment methods limited?

**Business Opportunity**: Even 1% improvement = huge revenue impact.

---

### Q4.3: Purchase Source "Other"
**Question**: What does `PURCHASE_SOURCE = 'other'` mean?

**Table**: `iap`

**Distribution**: Vast majority are "other"

**Other Values**: "rewarded_ad", "offer_wall", "shop"

**Impact**: Cannot properly attribute purchase triggers.

---

### Q4.4: DMP Integration
**Question**: What DMP (Data Management Platform) is integrated?

**Context**: `HAS_DMP_DATA` is always true in sessions table

**Details Needed**:
- What DMP provider?
- What data do they provide?
- How is it used for targeting/optimization?
- Can we access this DMP data?

---

### Q4.5: Signal Ads
**Question**: What are "signal ads" mentioned in notes?

**Context**: "Signal ads - e.g. fake ad for a project to get a sense of information. e.g. brand choice ads. Opportunity to run tests."

**Details Needed**:
- How common are signal ads?
- Are they tracked differently?
- What data do they collect?
- How are they used?

---

## Priority 5: LOW - Technical Details

### Q5.1: N8 System
**Question**: What is the "N8" system referenced in tracker_events?

**Field**: `USED_N8` (always false in sample)

**Hypotheses**:
- Internal system name?
- Partner integration?
- Deprecated feature?

---

### Q5.2: ZBD Integration Details
**Question**: How does ZEBEDEE (crypto) integration work?

**Fields**: `ZBD_MILLISATS_REWARD`, `ZBD_GAMERTAG`, `ZBD_USER_ID`

**Context**: Bitcoin Lightning rewards for watching ads

**Details Needed**:
- What percentage of users use ZBD?
- How does reward amount vary?
- Is this an experiment or permanent feature?

---

### Q5.3: Video Parsing
**Question**: What does `SDK_VAST_PARSING` indicate?

**Table**: `bids`

**Context**: VAST = Video Ad Serving Template

**Details Needed**:
- Does SDK parse VAST XML or does server?
- Impact on video ad performance?

---

### Q5.4: Batch Numbers
**Question**: What is `BATCH_NUMBER` in impressions table?

**Hypothesis**: Batch ad requests (SDK requests multiple ads at once)?

**Details Needed**:
- How many ads per batch typically?
- Does batching improve performance/revenue?

---

## Priority 6: CRITICAL - Data Availability & Access

### Q6.1: Historical Data Depth
**Question**: How much historical data is available?

**Sample**: Shows 24 hours of data (Sept 15, 2025)

**Need to Know**:
- How far back does data go? (6 months? 1 year? 5 years?)
- Is historical data complete or sampled?
- Any data gaps or quality issues in older data?

**Business Impact**: More history = better ML training, better trend analysis.

---

### Q6.2: Production Data Scale
**Question**: What is the true production data volume?

**Sample Analysis Scenarios**:
- Sample = 1% of production → 100x scale (32GB/day)
- Sample = 0.1% of production → 1000x scale (323GB/day)

**Need**: Actual daily event counts per table.

**Business Impact**: Affects pricing, infrastructure requirements.

---

### Q6.3: Data Refresh Frequency
**Question**: How often is data updated/available?

**Options**:
- Real-time streaming?
- Hourly batches?
- Daily batches?
- Weekly dumps?

**Business Impact**: Affects buyer use cases (real-time vs historical analysis).

---

### Q6.4: Sample Representativeness
**Question**: Is the provided sample representative of production?

**Concerns**:
- Geographic distribution (sample shows many redacted US addresses)
- Game distribution (which games are included?)
- Time period (Sept 15 - typical day or anomalous?)
- Device distribution

**Need**: Confirmation that sample accurately reflects production distributions.

---

## Priority 7: CRITICAL - Privacy & Compliance

### Q7.1: Data Sharing Permissions
**Question**: Do we have legal right to resell this data?

**Critical**: Must confirm with legal team and Adinmo.

**Details Needed**:
- User consent language (what did users agree to?)
- Privacy policy terms
- Data processing agreements with Adinmo
- Any restrictions on downstream use

---

### Q7.2: PII Handling
**Question**: Which fields are considered PII and must remain redacted?

**Currently Redacted** (in sample):
- IP_ADDRESS
- ADVERTISING_ID
- USER_AGENT
- Specific geo fields (STATE, CITY, POSTCODE)

**Clarifications Needed**:
- Can we provide IP addresses in hashed form?
- Can we provide country-level geo without full address?
- Can we provide device fingerprints without actual IDFA/GAID?

---

### Q7.3: GDPR Compliance Strategy
**Question**: How do we ensure GDPR compliance when reselling?

**Observed**: 
- CONSENT_GDPR field is 91-94% null in most tables
- When present, mix of true/false

**Strategies**:
1. Only provide data for consented users (filter CONSENT_GDPR = true)
2. Anonymize further (remove more fields)
3. Aggregate to cohort level

**Need**: Legal guidance on which approach is required.

---

### Q7.4: Attribution Partner Data Sharing
**Question**: Do attribution partners (Singular, AppsFlyer, Adjust) allow data resale?

**Context**: `attributed_installs` data comes from these partners.

**Risk**: Partners may have contractual restrictions on data sharing.

**Action**: Review partner agreements for data sharing clauses.

---

## Priority 8: Business Context Questions

### Q8.1: Campaign Cost Data
**Question**: Is campaign spend/cost data available?

**Why Important**: Need cost data to calculate true ROI.

**Current State**: We have installs and revenue, but not campaign costs.

**Workaround**: Buyers provide their own cost data and join?

---

### Q8.2: Creative Asset Access
**Question**: Can we access actual creative assets (images/videos)?

**Context**: We have `IMAGE_GUID` references to creatives.

**Use Cases**:
- Creative analysis (what visual elements work?)
- ML models trained on creative content
- Brand safety analysis

---

### Q8.3: Game Metadata
**Question**: Is there metadata about games (genre, publisher, etc.)?

**Current State**: We have `GAME_ID` but minimal metadata.

**Needed**:
- Game name
- Genre
- Publisher
- Release date
- Price (free vs paid)

---

## Recommended Next Steps

### Immediate Actions (Before Data Resale)

1. **Schedule Call with Adinmo Team**
   - Walk through Priority 1 & Priority 2 questions
   - Document answers formally
   - Record call for reference

2. **Legal Review**
   - Review all Priority 7 questions with legal counsel
   - Verify data sharing permissions
   - Draft buyer data use agreements

3. **Technical Validation**
   - Run SQL queries to validate hypotheses
   - Check for data consistency issues
   - Document any data quality issues

4. **Create Data Dictionary**
   - Incorporate answers into formal documentation
   - Provide to buyers for transparency
   - Include known limitations

### Ongoing Due Diligence

1. **Monitor Data Quality**
   - Track null rates over time (are they increasing?)
   - Identify new anomalies
   - Alert on unexpected changes

2. **Buyer Feedback Loop**
   - Collect questions from early buyers
   - Feed back to Adinmo for clarification
   - Update documentation continuously

3. **Competitive Intelligence**
   - How do other gaming datasets handle these issues?
   - What's industry standard for attribution windows?
   - Benchmark against other data products

---

## Question Tracking Template

For each question, we should track:

```yaml
question_id: Q1.1
category: Data Integrity
priority: CRITICAL
status: [PENDING | ASKED | ANSWERED | PARTIALLY_ANSWERED]
asked_date: YYYY-MM-DD
answered_date: YYYY-MM-DD
answer_source: [Yavuz | Documentation | SQL Analysis | Inference]
answer: |
  [Documented answer]
impact: |
  [Business impact of answer]
follow_up_needed: [YES | NO]
follow_up_questions: |
  [If additional questions arose from answer]
```

---

## Summary Statistics

- **Total Questions**: 50+
- **Priority 1 (Critical)**: 4 questions
- **Priority 2 (High)**: 5 questions
- **Priority 3-5 (Medium-Low)**: 20+ questions
- **Priority 6 (Data Access)**: 4 questions
- **Priority 7 (Legal/Privacy)**: 4 questions

**Recommendation**: Focus on Priority 1-2 (9 questions) before any data sales occur. These are foundational to understanding the dataset.


# Adinmo Data Relationships & Entity Model

## Overview
The Adinmo dataset consists of 6 interconnected tables that capture the complete user journey from ad request to app install to monetization. The data model is designed around **ANON_DEVICE_ID** as the central linking key.

## Primary Linking Keys

### 1. ANON_DEVICE_ID (Universal User Identifier)
- **Purpose**: THE central identifier linking all user activity
- **Scope**: Unique per device, per game
- **Privacy**: Anonymized/hashed to protect user identity
- **Present in**: ALL 6 tables
- **Cardinality**: High (one per user per game)
- **Business Critical**: Enables complete user journey reconstruction

### 2. SESSION_ID (Activity Container)
- **Purpose**: Groups all events within a single app session
- **Scope**: Unique per app open/launch
- **Present in**: bids, impressions, iap, sessions, tracker_events, attributed_installs
- **Lifecycle**: Created on session_start, used until session end/timeout
- **Business Use**: Frequency capping, session-level monetization

### 3. GAME_ID (Content Context)
- **Purpose**: Identifies which game/app the event occurred in
- **Scope**: Low cardinality (~5-10 games)
- **Present in**: ALL 6 tables
- **Business Use**: Game-level performance comparison, portfolio analysis

## Entity Relationship Diagram

```
┌──────────────┐
│   SESSIONS   │  (Session Start)
│              │
│ SESSION_ID◄──┼────────────────────────────────┐
│ ANON_DEVICE  │                                │
└──────┬───────┘                                │
       │                                        │
       │ 1:N                                    │
       ▼                                        │
┌──────────────┐                                │
│     BIDS     │  (Ad Request)                  │
│              │                                │
│ BID_ID       │                                │
│ SESSION_ID   │                                │
│ ANON_DEVICE  │                                │
└──────┬───────┘                                │
       │                                        │
       │ 1:N                                    │
       ▼                                        │
┌──────────────┐                                │
│ IMPRESSIONS  │  (Ad Shown)                    │
│              │                                │
│ IMPRESSION_ID│◄─────┐                         │
│ BID_ID       │      │                         │
│ SESSION_ID   │      │ N:1                     │
│ ANON_DEVICE  │      │                         │
└──────────────┘      │                         │
                      │                         │
              ┌───────┴──────┐                  │
              │              │                  │
       ┌──────▼──────┐ ┌─────▼─────┐           │
       │   TRACKER   │ │    IAP    │           │
       │   EVENTS    │ │           │           │
       │             │ │SESSION_ID │           │
       │IMPRESSION_ID│ │ANON_DEVICE│           │
       │ SESSION_ID  │ │CAMPAIGN_ID│           │
       │ ANON_DEVICE │ │IMAGE_GUID │           │
       └─────────────┘ └───────────┘           │
                                                │
                      ┌─────────────────────────┘
                      │
               ┌──────▼─────────┐
               │  ATTRIBUTED    │
               │   INSTALLS     │
               │                │
               │  SESSION_ID    │
               │  ANON_DEVICE   │
               │  CAMPAIGN_ID   │
               │  IMAGE_GUID    │
               └────────────────┘
```

## Table Relationships Detailed

### Sessions → Bids (1:N)
- **Relationship**: One session contains multiple bid requests
- **Join**: `sessions.SESSION_ID = bids.SESSION_ID`
- **Business Logic**: Users see multiple ads during a gaming session
- **Typical Ratio**: 5-20 bids per session (depends on session length)

### Bids → Impressions (1:N)
- **Relationship**: One bid can result in multiple impression attempts
- **Join**: `bids.BID_ID = impressions.BID_ID`
- **Business Logic**: A bid may lead to valid, invalid, or multiple impressions
- **Typical Ratio**: 0-2 impressions per bid (many bids don't result in impressions)

### Impressions → Tracker Events (1:N)
- **Relationship**: One impression generates multiple tracking events
- **Join**: `impressions.IMPRESSION_ID = tracker_events.IMPRESSION_ID`
- **Business Logic**: render → impression → [optional: click, magnify, video events]
- **Typical Ratio**: 2-10 events per impression (depends on ad type and engagement)

### Sessions → IAP (1:N)
- **Relationship**: Multiple purchase attempts per session
- **Join**: `sessions.SESSION_ID = iap.SESSION_ID`
- **Business Logic**: Users may attempt purchases during gameplay
- **Typical Ratio**: 0-5 IAP attempts per session (most sessions have 0)

### Tracker Events (click) → Attributed Installs (1:1)
- **Relationship**: Click events that lead to app installs
- **Join**: Complex - requires `ANON_DEVICE_ID` + time window + campaign matching
- **Business Logic**: User clicks ad → installs advertised app within attribution window
- **Typical Ratio**: 1-10% of clicks result in attributed installs

### Attributed Installs → Sessions (1:1)
- **Relationship**: First session after install
- **Join**: `attributed_installs.SESSION_ID = sessions.SESSION_ID`
- **Business Logic**: Track post-install behavior
- **Business Value**: Calculate install-to-purchase conversion, LTV

## Cross-Table User Journey Patterns

### Pattern 1: Complete Ad Monetization Funnel
```sql
-- User sees ad and monetizes via ad click
SELECT 
  s.SESSION_ID,
  s.ANON_DEVICE_ID,
  b.BID_ID,
  i.IMPRESSION_ID,
  te.EVENT_TYPE,
  ai.INSTALL_TS
FROM sessions s
JOIN bids b ON s.SESSION_ID = b.SESSION_ID
JOIN impressions i ON b.BID_ID = i.BID_ID
JOIN tracker_events te ON i.IMPRESSION_ID = te.IMPRESSION_ID
LEFT JOIN attributed_installs ai ON s.ANON_DEVICE_ID = ai.ANON_DEVICE_ID
WHERE te.EVENT_TYPE = 'click'
ORDER BY s.ACTIVITY_TS;
```

### Pattern 2: Organic IAP Monetization
```sql
-- User makes purchase without ad influence
SELECT 
  s.SESSION_ID,
  s.ANON_DEVICE_ID,
  COUNT(DISTINCT i.IMPRESSION_ID) as ads_seen,
  SUM(CASE WHEN iap.IAP_PURCHASE_MADE THEN 1 ELSE 0 END) as purchases,
  SUM(iap.AMOUNT_INVOICEABLE) as revenue
FROM sessions s
LEFT JOIN impressions i ON s.SESSION_ID = i.SESSION_ID
LEFT JOIN iap ON s.SESSION_ID = iap.SESSION_ID
GROUP BY 1, 2
HAVING purchases > 0;
```

### Pattern 3: Cross-Game Attribution
```sql
-- User sees ad in Game A, installs Game B
SELECT 
  g1.GAME_NAME as source_game,
  g2.GAME_NAME as installed_game,
  ai.CAMPAIGN_ID,
  COUNT(*) as installs,
  AVG(TIMESTAMPDIFF(HOUR, ai.ACTIVITY_TS, ai.INSTALL_TS)) as avg_hours_to_install
FROM attributed_installs ai
JOIN games g1 ON ai.GAME_ID = g1.GAME_ID
JOIN sessions s_new ON ai.SESSION_ID = s_new.SESSION_ID
JOIN games g2 ON s_new.GAME_ID = g2.GAME_ID
GROUP BY 1, 2, 3;
```

### Pattern 4: Ad-Influenced IAP (Brand Lift)
```sql
-- Did seeing ad increase purchase likelihood?
WITH ad_exposed AS (
  SELECT DISTINCT 
    s.ANON_DEVICE_ID,
    i.CAMPAIGN_ID,
    MIN(i.ACTIVITY_TS) as first_ad_exposure
  FROM sessions s
  JOIN impressions i ON s.SESSION_ID = i.SESSION_ID
),
purchases AS (
  SELECT 
    iap.ANON_DEVICE_ID,
    iap.ACTIVITY_TS as purchase_ts,
    SUM(iap.AMOUNT_INVOICEABLE) as revenue
  FROM iap
  WHERE iap.IAP_PURCHASE_MADE = true
  GROUP BY 1, 2
)
SELECT 
  ae.CAMPAIGN_ID,
  COUNT(DISTINCT ae.ANON_DEVICE_ID) as users_exposed,
  COUNT(DISTINCT p.ANON_DEVICE_ID) as users_purchased,
  SUM(p.revenue) as attributed_revenue
FROM ad_exposed ae
LEFT JOIN purchases p 
  ON ae.ANON_DEVICE_ID = p.ANON_DEVICE_ID
  AND p.purchase_ts > ae.first_ad_exposure
  AND p.purchase_ts < DATE_ADD(ae.first_ad_exposure, INTERVAL 7 DAY)
GROUP BY 1;
```

## Data Lineage & Timing

### Temporal Ordering (ACTIVITY_TS field in all tables)
1. **sessions.ACTIVITY_TS**: Session starts (earliest event)
2. **bids.ACTIVITY_TS**: Ad request made (seconds after session start)
3. **impressions.ACTIVITY_TS**: Ad shown (milliseconds after bid)
4. **tracker_events.ACTIVITY_TS**: User interactions (during/after impression)
5. **attributed_installs.ACTIVITY_TS**: Click/impression that led to install
6. **attributed_installs.INSTALL_TS**: Actual install (hours/days after click)
7. **iap.ACTIVITY_TS**: Purchase attempts (anytime during session)

### Key Timing Insights
- **Bid to Impression**: <100ms (real-time bidding)
- **Impression to Click**: 1-30 seconds (user decision time)
- **Click to Install**: Minutes to days (attribution window)
- **Install to Purchase**: Days to weeks (LTV analysis)

## Common Keys Summary

| Key | Tables | Cardinality | Purpose |
|-----|--------|-------------|---------|
| **ANON_DEVICE_ID** | ALL 6 | High | User identity |
| **SESSION_ID** | ALL 6 | High | Session grouping |
| **GAME_ID** | ALL 6 | Low (~10) | Game context |
| **BID_ID** | bids, impressions, tracker_events | High | Bid tracking |
| **IMPRESSION_ID** | impressions, tracker_events | High | Impression tracking |
| **CAMPAIGN_ID** | bids, impressions, iap, tracker_events, attributed_installs | Medium | Campaign tracking |
| **IMAGE_GUID** | impressions, iap, attributed_installs | Medium | Creative tracking |

## Data Integrity Considerations

### Orphaned Records Scenarios
1. **Bids without Impressions**: No ad fill, bid rejected
2. **Impressions without Tracker Events**: Tracking failure, invalid impression
3. **Clicks without Attributed Installs**: User didn't install, outside attribution window
4. **Sessions without Bids**: User played but no ads requested
5. **IAP without Impressions**: Organic monetization

### Duplicate Detection Keys
- **INSERT_ID**: Unique per row (primary key)
- **BID_ID**: Unique per bid request
- **IMPRESSION_ID**: Unique per impression
- **SESSION_ID**: Unique per session
- **ANON_DEVICE_ID**: NOT unique (appears in multiple events)

## Advanced Relationship Patterns

### Many-to-Many Relationships

#### Users ↔ Games (via ANON_DEVICE_ID x GAME_ID)
- Users can play multiple games
- Each game has multiple users
- ANON_DEVICE_ID is per-user-per-game
- Cross-game analysis requires additional logic

#### Campaigns ↔ Creatives (via CAMPAIGN_ID x IMAGE_GUID)
- Campaigns have multiple creative assets
- Creatives can be reused across campaigns
- Performance comparison critical

### Temporal Relationships

#### Session Sequence Analysis
```sql
-- Calculate session frequency per user
SELECT 
  ANON_DEVICE_ID,
  GAME_ID,
  COUNT(*) as total_sessions,
  MIN(ACTIVITY_TS) as first_session,
  MAX(ACTIVITY_TS) as last_session,
  DATEDIFF(MAX(ACTIVITY_TS), MIN(ACTIVITY_TS)) as days_active,
  COUNT(*) / NULLIF(DATEDIFF(MAX(ACTIVITY_TS), MIN(ACTIVITY_TS)), 0) as sessions_per_day
FROM sessions
GROUP BY 1, 2
HAVING total_sessions > 1;
```

#### Event Sequence Within Session
```sql
-- Order all events within a session
SELECT 
  SESSION_ID,
  'session_start' as event_type,
  ACTIVITY_TS,
  1 as event_order
FROM sessions
UNION ALL
SELECT 
  SESSION_ID,
  'bid_request',
  ACTIVITY_TS,
  2
FROM bids
UNION ALL
SELECT 
  SESSION_ID,
  'impression',
  ACTIVITY_TS,
  3
FROM impressions
UNION ALL
SELECT 
  SESSION_ID,
  EVENT_TYPE,
  ACTIVITY_TS,
  4
FROM tracker_events
UNION ALL
SELECT 
  SESSION_ID,
  'iap_attempt',
  ACTIVITY_TS,
  5
FROM iap
ORDER BY SESSION_ID, ACTIVITY_TS;
```

## Relationship Strength & Data Quality

### Strong Relationships (High Join Success Rate)
- **sessions → bids**: 90%+ (most sessions have bid requests)
- **bids → impressions**: 40-60% (fill rate dependent)
- **impressions → tracker_events**: 80%+ (tracking usually works)

### Weak Relationships (Low Join Success Rate)
- **tracker_events (clicks) → attributed_installs**: 2-10% (low install rate)
- **sessions → iap (successful)**: 1-5% (low purchase rate)
- **impressions → iap (attributed)**: <1% (direct ad-to-purchase)

## Critical Questions for Relationship Validation

1. **Can one SESSION_ID span multiple ANON_DEVICE_IDs?** (should be NO)
2. **Can one BID_ID have multiple IMPRESSION_IDs?** (YES - retries)
3. **Can one IMPRESSION_ID have clicks from different users?** (should be NO)
4. **Do all attributed_installs have corresponding click tracker_events?** (SHOULD, validate)
5. **Are there sessions with IAP but no impressions?** (YES - organic monetization)
6. **Can ANON_DEVICE_ID appear in multiple GAMEs?** (DESIGN QUESTION)

## Next Steps for Relationship Validation

1. **Run join coverage analysis**: What % of records successfully join?
2. **Identify orphan records**: Which records have no related records?
3. **Validate temporal ordering**: Are events in logical time sequence?
4. **Check referential integrity**: Do all foreign keys point to existing records?
5. **Analyze cardinality**: Do ratios match expected business logic?


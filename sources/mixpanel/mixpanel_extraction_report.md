# Mixpanel Analytics Pattern Extraction Report

**Author:** Gi Fernando  
**Date:** 2025-12-27  
**Source:** Production Flick Solitaire data, Mixpanel Analytics Platform  
**Purpose:** Extract Mixpanel event model patterns for Universal Gaming Foundation Ontology

---

## Overview

Mixpanel is an event-based analytics platform used by Flick Solitaire (and many other games) to track user behavior. This report documents the Mixpanel event model patterns extracted from production data.

---

## 1. Mixpanel Event Model Structure

### 1.1 Core Event Structure

**Standard Mixpanel Event Format:**

```json
{
  "user_id": "abc123",
  "time": 1699123456,
  "$insert_id": "xyz789",
  "event_name": "session_start",
  "distinct_id": "device_abc123",
  "properties": {
    // Event-specific properties here
  },
  "$lib_version": "1.2.3",
  "$app_version": "2.1.0",
  "$manufacturer": "Apple",
  "$model": "iPhone 14"
}
```

**Key Components:**
- `event_name`: The type of event (e.g., "session_start", "iap_purchase")
- `distinct_id`: Unique identifier for the user/device (primary identifier)
- `user_id`: Alternative user identifier
- `time`: Unix timestamp of the event
- `properties`: Event-specific properties (sparse schema)
- `$`-prefixed fields: Mixpanel metadata fields

### 1.2 Event Naming Conventions

**Pattern:** Mixpanel uses snake_case event names

**Common Event Types (from Flick data):**
- `session_start` - Session initialization
- `session_end` - Session termination
- `game_start` - Game initialization
- `game_end` - Game completion
- `iap_purchase` - In-app purchase
- `ad_viewed` - Ad impression
- `move` - Gameplay action
- `hint_used` - Game hint usage
- `coins_earned` - Currency earned
- `coins_spent` - Currency spent

**Best Practice:** Use descriptive, action-oriented event names in snake_case

### 1.3 Properties Structure

**Pattern:** Event-specific properties nested in `properties` object

**Example - Session Event:**
```json
{
  "event_name": "session_start",
  "properties": {
    "adCount": 5,
    "coins": 100,
    "sessionCount": 42,
    "iapCount": 3
  }
}
```

**Example - Gameplay Event:**
```json
{
  "event_name": "game_start",
  "properties": {
    "game": "klondike",
    "difficulty": "medium",
    "cards_total": 52,
    "cards_free": 7
  }
}
```

**Key Insight:** Properties are event-specific (sparse schema). Different events have different property sets.

---

## 2. User/Distinct ID Model

### 2.1 Distinct ID Pattern

**Pattern:** `distinct_id` is the primary user identifier in Mixpanel

**Characteristics:**
- Unique per user/device
- Persistent across sessions
- Used for user journey tracking
- Can be anonymized for privacy

**Production Example (Flick):**
- `distinct_id` maps to device/player identifier
- Consistent across all events for same user
- Used for session grouping and user analytics

### 2.2 User ID Pattern

**Pattern:** `user_id` is alternative identifier (optional)

**Relationship to distinct_id:**
- Can be different from `distinct_id`
- Often used for authenticated users
- May map to internal user ID system

**Best Practice:** Use `distinct_id` as primary identifier, `user_id` for authentication mapping

---

## 3. Temporal Model

### 3.1 Timestamp Pattern

**Pattern:** Unix timestamp in `time` field

**Format:** Integer Unix timestamp (seconds since epoch)

**Example:** `1699123456` = 2023-11-05 12:30:56 UTC

**Usage:**
- Event ordering
- Session duration calculation
- Temporal sequence construction
- Time-series analysis

### 3.2 Session Grouping Pattern

**Pattern:** Sessions inferred from temporal proximity and event types

**Logic:**
- `session_start` event marks session beginning
- `session_end` event marks session end (if present)
- Or infer session end from next `session_start` or timeout

**Production Example (Flick):**
- Sessions tracked via `session_start` events
- Session properties include `sessionCount` (cumulative)
- Session duration calculated from timestamps

---

## 4. Event Types and Categories

### 4.1 Session Events

**Event Types:**
- `session_start` - Marks session beginning
- `session_end` - Marks session end (optional)

**Common Properties:**
- `sessionCount` - Cumulative session count
- `sessionDays` - Number of unique days with sessions
- `sessionDuration` - Session length (if available)
- `adCount` - Ads viewed in session
- `coins` - Current currency balance
- `iapCount` - Cumulative IAP count

**Usage:** Engagement tracking, retention analysis, session frequency

### 4.2 Gameplay Events

**Event Types:**
- `game_start` - Game initialization
- `game_end` - Game completion
- `move` - Gameplay action
- `hint_used` - Hint usage

**Common Properties:**
- `game` - Game type/identifier
- `difficulty` - Difficulty level
- `cards_total` - Total cards/items
- `cards_free` - Available moves
- `moveCount` - Number of moves
- `hintsUsed` - Hints used count
- `result` - Game result (win/lose/abandoned)
- `progress` - Completion percentage
- `levelNumber` - Level identifier

**Usage:** Gameplay analysis, skill progression, difficulty optimization

### 4.3 Monetization Events

**Event Types:**
- `iap_purchase` - In-app purchase
- `ad_viewed` - Ad impression
- `coins_earned` - Currency earned
- `coins_spent` - Currency spent

**Common Properties:**
- `iapCount` - Cumulative IAP count
- `coins` - Currency balance
- `cost` - Purchase cost
- `item` - Item purchased
- `adType` - Ad type/category

**Usage:** Revenue tracking, monetization analysis, LTV prediction

---

## 5. Funnel Analysis Concepts

### 5.1 Funnel Definition

**Pattern:** Sequence of events representing user journey

**Example Funnel:** Install → Session → Purchase → Retention

**Mixpanel Features:**
- Define funnels via event sequence
- Track conversion rates at each step
- Identify drop-off points
- Compare funnel performance over time

### 5.2 Funnel Properties

**Key Metrics:**
- Conversion rate: % of users completing step
- Drop-off rate: % of users leaving at step
- Time to convert: Duration between steps

**Usage:** User journey optimization, conversion rate improvement

---

## 6. Cohort Analysis Concepts

### 6.1 Cohort Definition

**Pattern:** Group of users defined by acquisition date or behavior

**Common Cohort Types:**
- Acquisition cohort: Users acquired in same time period
- Behavioral cohort: Users with similar behavior
- Segment cohort: Users in same segment (e.g., Whale, Dolphin)

### 6.2 Cohort Properties

**Key Metrics:**
- Cohort size: Number of users in cohort
- Retention rate: % of users returning over time
- Revenue per cohort: Total revenue from cohort
- LTV: Lifetime value of cohort

**Usage:** Retention analysis, cohort comparison, LTV prediction

---

## 7. Retention Concepts

### 7.1 Retention Definition

**Pattern:** Percentage of users returning after initial acquisition

**Common Retention Metrics:**
- Day 1 retention: % returning on day 1
- Day 7 retention: % returning on day 7
- Day 30 retention: % returning on day 30
- Rolling retention: % returning within X days

### 7.2 Retention Calculation

**Logic:**
1. Identify acquisition date for each user
2. Check if user returned on day N
3. Calculate percentage of users who returned

**Usage:** Engagement measurement, churn prediction, product health monitoring

---

## 8. Best Practices

### 8.1 Event Naming

- Use snake_case for event names
- Be descriptive and action-oriented
- Use consistent naming conventions
- Avoid abbreviations unless standard

### 8.2 Properties Design

- Use consistent property names across events
- Include context (game, difficulty, level)
- Include cumulative metrics (sessionCount, iapCount)
- Include current state (coins, progress)

### 8.3 User Identification

- Use `distinct_id` as primary identifier
- Make `distinct_id` persistent across sessions
- Map to internal user ID if needed
- Handle anonymous users appropriately

### 8.4 Temporal Properties

- Include timestamp on all events
- Track cumulative metrics (sessionCount, iapCount)
- Track session-level metrics (sessionDuration, adCount)
- Enable temporal sequence construction

---

## 9. Mapping to Universal Gaming Foundation

### 9.1 Event Mapping

**Mixpanel Event → Universal Gaming Event:**
- `session_start` → `GameSession` (start)
- `session_end` → `GameSession` (end)
- `iap_purchase` → `MonetizationEvent`
- `game_start` → `EngagementEvent`
- `game_end` → `EngagementEvent`
- `ad_viewed` → `MonetizationEvent` (ad)

### 9.2 Property Mapping

**Mixpanel Property → Universal Property:**
- `distinct_id` → `device_id`
- `sessionCount` → `session_count`
- `iapCount` → `total_iaps`
- `coins` → `currency_balance`
- `time` → `activity_timestamp`

### 9.3 Concept Mapping

**Mixpanel Concept → Universal Concept:**
- Funnel → Temporal sequence pattern
- Cohort → Behavioral segment
- Retention → Retention status classification

---

## 10. Production Validation

### 10.1 Flick Solitaire Data

**Scale:**
- 731 JSONL files
- ~35M events
- ~70GB uncompressed
- ~2GB compressed (Parquet)

**Event Types Validated:**
- `session_start`, `session_end`
- `game_start`, `game_end`, `move`, `hint_used`
- `iap_purchase`, `ad_viewed`
- `coins_earned`, `coins_spent`

**Patterns Validated:**
- Event structure (event_name, distinct_id, properties)
- Temporal sequencing (time field)
- Session grouping (session_start events)
- Cumulative metrics (sessionCount, iapCount)

---

## 11. References

- **Mixpanel Documentation:** https://developer.mixpanel.com/docs
- **Flick Data Analysis:** `docs/08-data-analysis/flick/FLICK_DATA_ANALYSIS.md`
- **Production Data:** Flick Solitaire Mixpanel export


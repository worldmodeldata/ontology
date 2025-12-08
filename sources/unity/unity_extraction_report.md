# Unity Analytics Pattern Extraction Report

**Author:** Gi Fernando  
**Date:** 2025-12-27  
**Source:** Unity Analytics Platform Documentation  
**Purpose:** Extract Unity Analytics event schema patterns for Universal Gaming Foundation Ontology

---

## Overview

Unity Analytics is a comprehensive analytics platform integrated into Unity game engine. This report documents Unity Analytics event schema patterns based on industry-standard Unity Analytics implementation patterns.

---

## 1. Unity Analytics Event Schema

### 1.1 Standard Events

Unity Analytics provides a set of standard events that are automatically tracked:

**Core Standard Events:**
- `level_start` - Player starts a level
- `level_complete` - Player completes a level
- `level_fail` - Player fails a level
- `level_up` - Player levels up
- `tutorial_start` - Tutorial begins
- `tutorial_complete` - Tutorial completed
- `screen_view` - Screen/view viewed
- `store_opened` - Store opened
- `store_item_click` - Store item clicked
- `store_closed` - Store closed
- `purchase` - Purchase made (monetization event)

### 1.2 Custom Events

**Pattern:** Unity allows custom event tracking with arbitrary event names and parameters

**Custom Event Structure:**
```json
{
  "event_name": "custom_event_name",
  "timestamp": 1699123456,
  "user_id": "user_abc123",
  "session_id": "session_xyz789",
  "parameters": {
    "param1": "value1",
    "param2": 42,
    "param3": true
  }
}
```

**Best Practice:** Use descriptive, consistent naming conventions for custom events

---

## 2. Property Patterns

### 2.1 Standard Properties

**Common Properties Tracked Automatically:**
- `user_id` - Unique user identifier
- `session_id` - Session identifier
- `timestamp` - Event timestamp
- `platform` - Platform (iOS, Android, WebGL, etc.)
- `device_model` - Device model
- `device_type` - Device type (mobile, desktop, console)
- `os_version` - Operating system version
- `app_version` - Application version
- `country` - Country code
- `language` - Language code

### 2.2 Custom Parameters

**Pattern:** Custom parameters can be added to any event

**Parameter Types:**
- String
- Integer
- Float
- Boolean

**Common Custom Parameters:**
- `level_number` - Level identifier
- `difficulty` - Difficulty level
- `score` - Player score
- `duration` - Event duration
- `item_id` - Item identifier
- `item_type` - Item type/category
- `currency_amount` - Currency amount
- `currency_type` - Currency type

---

## 3. Event Hierarchy and Relationships

### 3.1 Level-Based Events

**Hierarchy:**
```
level_start
  ├─ level_complete
  │  └─ level_up (if applicable)
  └─ level_fail
```

**Pattern:** Level events form a hierarchy where completion/failure are children of start

### 3.2 Session-Based Events

**Pattern:** Events can be grouped by session_id

**Session Events:**
- `session_start` - Session begins
- `session_end` - Session ends
- All other events occur within a session

**Properties:**
- `session_id` - Links all events in same session
- `session_duration` - Time in session (for session_end)

### 3.3 Purchase/Monetization Events

**Pattern:** Purchase events follow a funnel

**Funnel:**
```
store_opened
  ├─ store_item_click
  └─ purchase (if completed)
```

**Purchase Event Properties:**
- `product_id` - Product identifier
- `product_type` - Product type
- `currency` - Currency code
- `amount` - Purchase amount
- `transaction_id` - Transaction identifier

---

## 4. User Identification Patterns

### 4.1 User ID Model

**Pattern:** Unity uses `user_id` as primary identifier

**Characteristics:**
- Unique per user/device
- Persistent across sessions
- Can be anonymous (random UUID) or authenticated (account ID)
- Used for user journey tracking

### 4.2 Session ID Model

**Pattern:** Unity uses `session_id` to group events

**Characteristics:**
- Unique per session
- Changes between sessions
- Links events that occur in same session
- Used for session-level analytics

---

## 5. Temporal Patterns

### 5.1 Timestamp Format

**Pattern:** Unix timestamp (seconds since epoch)

**Format:** Integer Unix timestamp

**Example:** `1699123456` = 2023-11-05 12:30:56 UTC

### 5.2 Session Duration Calculation

**Pattern:** Calculate duration from session_start and session_end events

**Logic:**
```
session_duration = session_end.timestamp - session_start.timestamp
```

**Alternative:** If session_end not tracked, infer from next session_start or timeout

---

## 6. Best Practices

### 6.1 Event Naming

- Use snake_case for event names
- Be descriptive and action-oriented
- Use consistent naming conventions
- Follow Unity standard event names where applicable

### 6.2 Property Design

- Use consistent property names across events
- Include context (level, difficulty, score)
- Include identifiers (item_id, product_id)
- Track cumulative metrics (total_score, total_purchases)

### 6.3 User Identification

- Make `user_id` persistent across sessions
- Use `session_id` for session grouping
- Handle anonymous vs authenticated users
- Support user authentication state changes

---

## 7. Mapping to Universal Gaming Foundation

### 7.1 Event Mapping

**Unity Event → Universal Gaming Event:**
- `level_start` → `EngagementEvent` (LevelStart)
- `level_complete` → `EngagementEvent` (LevelComplete)
- `level_fail` → `EngagementEvent` (LevelFail)
- `purchase` → `MonetizationEvent` (Purchase)
- `store_opened` → `EngagementEvent` (StoreOpened)
- `session_start` → `GameSession` (start)
- `session_end` → `GameSession` (end)

### 7.2 Property Mapping

**Unity Property → Universal Property:**
- `user_id` → `device_id`
- `session_id` → `session_id`
- `timestamp` → `activity_timestamp`
- `level_number` → `level_number`
- `product_id` → `item_id`
- `amount` → `amount`

### 7.3 Concept Mapping

**Unity Concept → Universal Concept:**
- Level-based events → Progression events
- Purchase events → Monetization events
- Session events → Game session events

---

## 8. Unity Analytics vs Mixpanel Comparison

### 8.1 Similarities

- Event-based tracking
- Custom event support
- User/session identification
- Timestamp-based temporal model
- Property/parameter flexibility

### 8.2 Differences

| Aspect | Unity Analytics | Mixpanel |
|--------|----------------|----------|
| Event Structure | Flat structure | Nested properties |
| Standard Events | Game-focused | Analytics-focused |
| Platform Integration | Unity-native | SDK-based |
| Metadata Prefix | None | `$` prefix |

---

## 9. Integration Considerations

### 9.1 Unity Engine Integration

- Events tracked automatically by Unity Analytics SDK
- Custom events via C# API
- Real-time event streaming
- Batch event upload

### 9.2 Data Export

- Unity Analytics Dashboard
- Data export API
- Raw event data export
- Aggregated analytics export

---

## 10. References

- **Unity Analytics Documentation:** https://docs.unity.com/analytics/
- **Unity Analytics Standard Events:** Unity Analytics SDK documentation
- **Industry Best Practices:** Unity Analytics community guidelines


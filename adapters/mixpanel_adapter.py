#!/usr/bin/env python3
"""
Mixpanel Analytics Adapter

Transforms Mixpanel Analytics data to universal gaming foundation ontology format.

Author: Gi Fernando
Copyright: © 2025 Gi Fernando. All rights reserved.
Date: 2025-12-27
"""

from game_source_adapter_template import GameSourceAdapter
from typing import Dict, Any, Optional
from datetime import datetime


class MixpanelAdapter(GameSourceAdapter):
    """
    Adapter for Mixpanel events.
    
    Maps Mixpanel events to universal gaming foundation format.
    Based on production Flick Solitaire data patterns.
    """
    
    def map_event_type(self, source_event: Dict[str, Any]) -> str:
        """Map Mixpanel event type to universal gaming event type."""
        event_name = source_event.get("event_name", "").lower()
        
        # Mixpanel event patterns (from Flick data)
        if event_name == "session_start":
            return "GameSession"  # Type: "SessionStart"
        elif event_name == "session_end":
            return "GameSession"  # Type: "SessionEnd"
        elif event_name == "game_start":
            return "EngagementEvent"  # Type: "GameStart"
        elif event_name == "game_end":
            return "EngagementEvent"  # Type: "GameEnd"
        elif event_name == "iap_purchase":
            return "MonetizationEvent"  # Type: "Purchase"
        elif event_name == "ad_viewed":
            return "MonetizationEvent"  # Type: "AdViewed"
        elif event_name == "move":
            return "EngagementEvent"  # Type: "Move"
        elif event_name == "hint_used":
            return "EngagementEvent"  # Type: "HintUsed"
        elif event_name == "coins_earned":
            return "MonetizationEvent"  # Type: "CoinsEarned"
        elif event_name == "coins_spent":
            return "MonetizationEvent"  # Type: "CoinsSpent"
        
        # Default
        return "GameEvent"
    
    def map_identifier(self, source_event: Dict[str, Any], identifier_type: str) -> Optional[str]:
        """Map Mixpanel identifier properties."""
        if identifier_type == "device_id":
            # Mixpanel uses distinct_id as primary identifier
            return source_event.get("distinct_id") or source_event.get("distinctId") or source_event.get("user_id")
        elif identifier_type == "session_id":
            # Mixpanel may not have explicit session_id, derive from properties
            props = source_event.get("properties", {})
            return props.get("session_id") or props.get("sessionId")
        elif identifier_type == "game_id":
            # Mixpanel may have app identifier in properties
            props = source_event.get("properties", {})
            return props.get("game_id") or props.get("app_id")
        
        return None
    
    def map_timestamp(self, source_event: Dict[str, Any]) -> datetime:
        """Map Mixpanel timestamp to datetime."""
        # Mixpanel uses "time" field (Unix timestamp in seconds)
        timestamp = source_event.get("time") or source_event.get("timestamp")
        
        if timestamp:
            if isinstance(timestamp, (int, float)):
                # Mixpanel typically uses seconds
                return datetime.fromtimestamp(timestamp)
            elif isinstance(timestamp, str):
                try:
                    return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    pass
        
        return datetime.now()
    
    def map_properties(self, source_event: Dict[str, Any]) -> Dict[str, Any]:
        """Map Mixpanel properties to universal properties."""
        properties = {}
        source_props = source_event.get("properties", {})
        
        # Mixpanel property mappings (from Flick data patterns)
        property_mappings = {
            # Session properties
            "sessionCount": "session_count",
            "session_count": "session_count",
            "sessionDays": "session_days",
            "sessionDuration": "session_duration",
            "adCount": "ad_view_count",
            "sessionAdCount": "session_ad_count",
            "timeSinceLastAd": "time_since_last_ad",
            
            # Monetization properties
            "iapCount": "total_iaps",
            "iap_count": "total_iaps",
            "coins": "currency_balance",
            "cost": "amount",
            "item": "item_id",
            "adType": "ad_type",
            "adRev_total": "ad_revenue_total",
            
            # Gameplay properties
            "game": "game_type",
            "difficulty": "difficulty",
            "cards_total": "cards_total",
            "cards_free": "cards_free",
            "moveCount": "move_count",
            "hintsUsed": "hints_used",
            "result": "game_result",
            "progress": "progress",
            "levelNumber": "level_number",
            
            # Mixpanel metadata (preserve)
            "$lib_version": "lib_version",
            "$app_version": "app_version",
            "$manufacturer": "manufacturer",
            "$model": "device_model",
            "$os": "device_os"
        }
        
        for mixpanel_key, universal_key in property_mappings.items():
            if mixpanel_key in source_props:
                properties[universal_key] = source_props[mixpanel_key]
        
        return properties


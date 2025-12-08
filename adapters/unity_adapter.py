#!/usr/bin/env python3
"""
Unity Analytics Adapter

Transforms Unity Analytics data to universal gaming foundation ontology format.

Author: Gi Fernando
Copyright: © 2025 Gi Fernando. All rights reserved.
Date: 2025-12-27
"""

from game_source_adapter_template import GameSourceAdapter
from typing import Dict, Any, Optional
from datetime import datetime


class UnityAnalyticsAdapter(GameSourceAdapter):
    """
    Adapter for Unity Analytics events.
    
    Maps Unity Analytics events to universal gaming foundation format.
    """
    
    def map_event_type(self, source_event: Dict[str, Any]) -> str:
        """Map Unity event type to universal gaming event type."""
        event_name = source_event.get("event_name", "").lower()
        
        # Unity standard events
        if event_name == "level_start":
            return "EngagementEvent"  # Type: "LevelStart"
        elif event_name == "level_complete":
            return "EngagementEvent"  # Type: "LevelComplete"
        elif event_name == "level_fail":
            return "EngagementEvent"  # Type: "LevelFail"
        elif event_name == "purchase":
            return "MonetizationEvent"  # Type: "Purchase"
        elif event_name == "store_opened":
            return "EngagementEvent"  # Type: "StoreOpened"
        elif event_name == "session_start":
            return "GameSession"  # Type: "SessionStart"
        elif event_name == "session_end":
            return "GameSession"  # Type: "SessionEnd"
        
        # Custom events - try to infer from name
        if "level" in event_name:
            return "EngagementEvent"
        elif "purchase" in event_name or "iap" in event_name:
            return "MonetizationEvent"
        elif "session" in event_name:
            return "GameSession"
        
        # Default
        return "GameEvent"
    
    def map_identifier(self, source_event: Dict[str, Any], identifier_type: str) -> Optional[str]:
        """Map Unity identifier properties."""
        if identifier_type == "device_id":
            # Unity uses user_id as primary identifier
            return source_event.get("user_id") or source_event.get("userId")
        elif identifier_type == "session_id":
            return source_event.get("session_id") or source_event.get("sessionId")
        elif identifier_type == "game_id":
            # Unity may have app_id or game_id
            return source_event.get("app_id") or source_event.get("game_id")
        
        return None
    
    def map_timestamp(self, source_event: Dict[str, Any]) -> datetime:
        """Map Unity timestamp to datetime."""
        timestamp = source_event.get("timestamp") or source_event.get("time")
        
        if timestamp:
            if isinstance(timestamp, (int, float)):
                if timestamp > 1e10:  # Milliseconds
                    return datetime.fromtimestamp(timestamp / 1000)
                else:  # Seconds
                    return datetime.fromtimestamp(timestamp)
            elif isinstance(timestamp, str):
                try:
                    return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    pass
        
        return datetime.now()
    
    def map_properties(self, source_event: Dict[str, Any]) -> Dict[str, Any]:
        """Map Unity properties to universal properties."""
        properties = {}
        source_props = source_event.get("parameters", {}) or source_event.get("properties", {})
        
        # Unity property mappings
        property_mappings = {
            "level_number": "level_number",
            "level_name": "level_name",
            "difficulty": "difficulty",
            "score": "score",
            "duration": "duration",
            "product_id": "item_id",
            "product_type": "item_type",
            "amount": "amount",
            "currency": "currency",
            "transaction_id": "transaction_id",
            "platform": "platform",
            "device_model": "device_type",
            "os_version": "os_version",
            "app_version": "app_version",
            "country": "country",
            "language": "language"
        }
        
        for unity_key, universal_key in property_mappings.items():
            if unity_key in source_props:
                properties[universal_key] = source_props[unity_key]
        
        return properties


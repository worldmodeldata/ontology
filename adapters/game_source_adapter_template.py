#!/usr/bin/env python3
"""
Generic Game Source Adapter Template

This template provides a framework for creating adapters that transform
game source data to universal gaming foundation ontology format.

Author: Gi Fernando
Copyright: © 2025 Gi Fernando. All rights reserved.
Date: 2025-12-27
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class GameSourceAdapter:
    """
    Template adapter for transforming game source data to universal gaming format.
    
    Subclass this class and implement the mapping methods for your specific game source.
    """
    
    def __init__(self, source_name: str, mapping_config: Dict[str, Any]):
        """
        Initialize the adapter.
        
        Args:
            source_name: Name of the game source (e.g., "MyGame", "AnotherGame")
            mapping_config: Configuration dictionary with mapping rules
        """
        self.source_name = source_name
        self.mapping_config = mapping_config
        
    # ========================================================================
    # Event Type Mapping
    # ========================================================================
    
    def map_event_type(self, source_event: Dict[str, Any]) -> str:
        """
        Map source event type to universal gaming event type.
        
        This method should:
        1. Extract event type from source event
        2. Match against known patterns (session, purchase, level, gameplay)
        3. Return universal event type
        
        Patterns to recognize:
        - Session events: session_start, session_end, session_begin, session_close
        - Purchase events: purchase, iap, transaction, buy, payment
        - Level events: level_start, level_complete, level_fail, level_begin, level_end
        - Gameplay events: game_start, game_end, move, action, play
        
        Args:
            source_event: Source event dictionary
            
        Returns:
            Universal event type (e.g., "GameSession", "MonetizationEvent", etc.)
        """
        raise NotImplementedError("Subclass must implement map_event_type")
    
    # ========================================================================
    # Property Mapping
    # ========================================================================
    
    def map_identifier(self, source_event: Dict[str, Any], identifier_type: str) -> Optional[str]:
        """
        Map identifier properties (user_id, device_id, session_id).
        
        Common source property names:
        - user_id: user_id, userId, user, uid, player_id, playerId
        - device_id: device_id, deviceId, device, did, device_uuid
        - session_id: session_id, sessionId, session, sid, session_uuid
        
        Args:
            source_event: Source event dictionary
            identifier_type: Type of identifier ("user_id", "device_id", "session_id")
            
        Returns:
            Identifier value or None if not found
        """
        raise NotImplementedError("Subclass must implement map_identifier")
    
    def map_timestamp(self, source_event: Dict[str, Any]) -> datetime:
        """
        Map timestamp property to datetime.
        
        Common source property names:
        - timestamp, time, date, ts, created_at, event_time
        
        Common formats:
        - Unix timestamp (seconds): 1699123456
        - Unix timestamp (milliseconds): 1699123456000
        - ISO 8601: "2023-11-05T12:30:56Z"
        - Custom format: depends on source
        
        Args:
            source_event: Source event dictionary
            
        Returns:
            datetime object
        """
        raise NotImplementedError("Subclass must implement map_timestamp")
    
    def map_properties(self, source_event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map all source properties to universal properties.
        
        Common mappings:
        - sessionCount, session_count -> session_count
        - iapCount, iap_count, total_iaps -> total_iaps
        - amount, cost, price -> amount
        - currency, currency_code -> currency
        
        Args:
            source_event: Source event dictionary
            
        Returns:
            Dictionary of mapped properties
        """
        raise NotImplementedError("Subclass must implement map_properties")
    
    # ========================================================================
    # Transformation Pipeline
    # ========================================================================
    
    def transform_event(self, source_event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a single source event to universal format.
        
        Universal format structure:
        {
            "event_id": str,
            "event_type": str,  # Universal event type
            "device_id": str,
            "session_id": Optional[str],
            "game_id": Optional[str],
            "activity_timestamp": datetime,
            "properties": Dict[str, Any]  # Universal properties
        }
        
        Args:
            source_event: Source event dictionary
            
        Returns:
            Universal format event dictionary
        """
        universal_event = {
            "event_id": self._generate_event_id(source_event),
            "event_type": self.map_event_type(source_event),
            "device_id": self.map_identifier(source_event, "device_id"),
            "session_id": self.map_identifier(source_event, "session_id"),
            "game_id": self.map_identifier(source_event, "game_id"),
            "activity_timestamp": self.map_timestamp(source_event),
            "properties": self.map_properties(source_event)
        }
        
        # Add source metadata
        universal_event["source_metadata"] = {
            "source_name": self.source_name,
            "original_event": source_event
        }
        
        return universal_event
    
    def transform_batch(self, source_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform a batch of source events.
        
        Args:
            source_events: List of source event dictionaries
            
        Returns:
            List of universal format event dictionaries
        """
        return [self.transform_event(event) for event in source_events]
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def _generate_event_id(self, source_event: Dict[str, Any]) -> str:
        """
        Generate unique event ID from source event.
        
        Uses source-specific identifier if available, otherwise generates UUID.
        
        Args:
            source_event: Source event dictionary
            
        Returns:
            Unique event ID string
        """
        # Try to find existing event ID in source
        event_id_keys = ["event_id", "id", "_id", "insert_id", "eventId"]
        for key in event_id_keys:
            if key in source_event:
                return str(source_event[key])
        
        # Generate new ID (in production, use UUID)
        import uuid
        return str(uuid.uuid4())
    
    def _normalize_property_name(self, source_property_name: str) -> str:
        """
        Normalize property name (snake_case conversion, etc.).
        
        Args:
            source_property_name: Original property name
            
        Returns:
            Normalized property name
        """
        # Convert camelCase to snake_case
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', source_property_name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    # ========================================================================
    # Validation
    # ========================================================================
    
    def validate_transformation(self, universal_event: Dict[str, Any]) -> bool:
        """
        Validate transformed event meets universal format requirements.
        
        Args:
            universal_event: Universal format event dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["event_id", "event_type", "device_id", "activity_timestamp"]
        return all(field in universal_event for field in required_fields)


# ============================================================================
# Example Implementation
# ============================================================================

class ExampleGameAdapter(GameSourceAdapter):
    """
    Example implementation of GameSourceAdapter.
    
    Replace with your specific game source implementation.
    """
    
    def map_event_type(self, source_event: Dict[str, Any]) -> str:
        """Map source event type to universal gaming event type."""
        event_name = source_event.get("event_name", "").lower()
        
        # Session events
        if "session" in event_name:
            if "start" in event_name or "begin" in event_name:
                return "GameSession"  # With type: "SessionStart"
            elif "end" in event_name or "close" in event_name:
                return "GameSession"  # With type: "SessionEnd"
        
        # Purchase events
        if any(keyword in event_name for keyword in ["purchase", "iap", "buy", "payment"]):
            return "MonetizationEvent"  # With type: "Purchase"
        
        # Level events
        if "level" in event_name:
            if "start" in event_name or "begin" in event_name:
                return "EngagementEvent"  # With type: "LevelStart"
            elif "complete" in event_name or "finish" in event_name:
                return "EngagementEvent"  # With type: "LevelComplete"
            elif "fail" in event_name:
                return "EngagementEvent"  # With type: "LevelFail"
        
        # Default to generic GameEvent
        return "GameEvent"
    
    def map_identifier(self, source_event: Dict[str, Any], identifier_type: str) -> Optional[str]:
        """Map identifier properties."""
        # Common property name variations
        identifier_mappings = {
            "device_id": ["device_id", "deviceId", "device", "user_id", "userId", "distinct_id"],
            "session_id": ["session_id", "sessionId", "session"],
            "game_id": ["game_id", "gameId", "game", "app_id", "appId"]
        }
        
        property_names = identifier_mappings.get(identifier_type, [])
        for prop_name in property_names:
            if prop_name in source_event:
                return str(source_event[prop_name])
        
        return None
    
    def map_timestamp(self, source_event: Dict[str, Any]) -> datetime:
        """Map timestamp property to datetime."""
        timestamp_keys = ["timestamp", "time", "date", "ts", "created_at"]
        
        for key in timestamp_keys:
            if key in source_event:
                timestamp_value = source_event[key]
                
                # Handle Unix timestamp (seconds)
                if isinstance(timestamp_value, (int, float)):
                    if timestamp_value > 1e10:  # Milliseconds
                        return datetime.fromtimestamp(timestamp_value / 1000)
                    else:  # Seconds
                        return datetime.fromtimestamp(timestamp_value)
                
                # Handle ISO 8601 string
                if isinstance(timestamp_value, str):
                    try:
                        return datetime.fromisoformat(timestamp_value.replace('Z', '+00:00'))
                    except ValueError:
                        continue
        
        # Default to current time if not found
        return datetime.now()
    
    def map_properties(self, source_event: Dict[str, Any]) -> Dict[str, Any]:
        """Map all source properties to universal properties."""
        properties = {}
        source_props = source_event.get("properties", {})
        
        # Property mappings
        property_mappings = {
            "sessionCount": "session_count",
            "session_count": "session_count",
            "iapCount": "total_iaps",
            "iap_count": "total_iaps",
            "total_iaps": "total_iaps",
            "amount": "amount",
            "cost": "amount",
            "price": "amount",
            "currency": "currency",
            "currency_code": "currency"
        }
        
        for source_key, universal_key in property_mappings.items():
            if source_key in source_props:
                properties[universal_key] = source_props[source_key]
        
        return properties


if __name__ == "__main__":
    # Example usage
    adapter = ExampleGameAdapter(
        source_name="ExampleGame",
        mapping_config={}
    )
    
    # Example source event
    source_event = {
        "event_name": "session_start",
        "user_id": "user123",
        "session_id": "session456",
        "timestamp": 1699123456,
        "properties": {
            "sessionCount": 42,
            "iapCount": 3
        }
    }
    
    # Transform event
    universal_event = adapter.transform_event(source_event)
    print(json.dumps(universal_event, indent=2, default=str))


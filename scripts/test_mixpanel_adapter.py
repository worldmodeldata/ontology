#!/usr/bin/env python3
"""
Test Mixpanel Adapter

Tests Mixpanel Analytics adapter transformation functionality.

Author: Gi Fernando
Copyright: © 2025 Gi Fernando. All rights reserved.
Date: 2025-12-27
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add adapters directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "adapters"))

from mixpanel_adapter import MixpanelAdapter


def test_mixpanel_adapter():
    """Test Mixpanel adapter with sample events."""
    adapter = MixpanelAdapter(
        source_name="Mixpanel",
        mapping_config={}
    )
    
    # Test events (based on Flick data patterns)
    test_events = [
        {
            "event_name": "session_start",
            "distinct_id": "device_abc123",
            "time": 1699123456,
            "properties": {
                "sessionCount": 42,
                "iapCount": 3,
                "coins": 100
            }
        },
        {
            "event_name": "iap_purchase",
            "distinct_id": "device_abc123",
            "time": 1699123500,
            "properties": {
                "iapCount": 4,
                "cost": 4.99,
                "item": "power_up"
            }
        },
        {
            "event_name": "game_start",
            "distinct_id": "device_abc123",
            "time": 1699123520,
            "properties": {
                "game": "klondike",
                "difficulty": "medium"
            }
        }
    ]
    
    print("Mixpanel Adapter Test")
    print("=" * 60)
    print()
    
    passed = 0
    failed = 0
    
    for i, test_event in enumerate(test_events, 1):
        print(f"Test Event {i}: {test_event['event_name']}")
        try:
            universal_event = adapter.transform_event(test_event)
            
            # Validate transformation
            if adapter.validate_transformation(universal_event):
                print(f"  ✅ Valid transformation")
                print(f"  Event Type: {universal_event['event_type']}")
                print(f"  Device ID: {universal_event['device_id']}")
                print(f"  Properties: {len(universal_event['properties'])} mapped")
                passed += 1
            else:
                print(f"  ❌ Invalid transformation")
                failed += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed += 1
        
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(test_mixpanel_adapter())


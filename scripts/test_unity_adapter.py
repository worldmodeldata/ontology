#!/usr/bin/env python3
"""
Test Unity Adapter

Tests Unity Analytics adapter transformation functionality.

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

from unity_adapter import UnityAnalyticsAdapter


def test_unity_adapter():
    """Test Unity Analytics adapter with sample events."""
    adapter = UnityAnalyticsAdapter(
        source_name="UnityAnalytics",
        mapping_config={}
    )
    
    # Test events
    test_events = [
        {
            "event_name": "level_start",
            "user_id": "user123",
            "session_id": "session456",
            "timestamp": 1699123456,
            "parameters": {
                "level_number": 5,
                "difficulty": "medium"
            }
        },
        {
            "event_name": "purchase",
            "user_id": "user123",
            "session_id": "session456",
            "timestamp": 1699123500,
            "parameters": {
                "product_id": "item001",
                "amount": 9.99,
                "currency": "USD"
            }
        },
        {
            "event_name": "session_start",
            "user_id": "user123",
            "timestamp": 1699123400
        }
    ]
    
    print("Unity Analytics Adapter Test")
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
    sys.exit(test_unity_adapter())


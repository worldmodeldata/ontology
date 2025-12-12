#!/usr/bin/env python3
"""
Adinmo Adapter (in-game ads + attribution telemetry)

Transforms Adinmo table rows into the universal gaming event dictionary format
used by our adapter framework.
"""

from typing import Dict, Any, Optional
from datetime import datetime

from game_source_adapter_template import GameSourceAdapter


class AdinmoAdapter(GameSourceAdapter):
    def map_event_type(self, source_event: Dict[str, Any]) -> str:
        table = (source_event.get("table") or "").lower().strip()
        event_type = (source_event.get("EVENT_TYPE") or source_event.get("event_type") or "").lower().strip()

        if table == "sessions":
            return "GameSession"
        if table == "bids":
            return "Bid"
        if table == "impressions":
            return "Impression"
        if table == "tracker_events":
            if event_type in {"click", "magnified"}:
                return "AdInteraction"
            if event_type.startswith("video_"):
                return "MonetizationEvent"
            return "AdEvent"
        if table == "attributed_installs":
            return "AttributedInstall"
        if table == "iap":
            return "InAppPurchase"
        return "GameEvent"

    def map_identifier(self, source_event: Dict[str, Any], identifier_type: str) -> Optional[str]:
        if identifier_type == "device_id":
            return source_event.get("ANON_DEVICE_ID") or source_event.get("anon_device_id")
        if identifier_type == "session_id":
            return source_event.get("SESSION_ID") or source_event.get("session_id")
        if identifier_type == "game_id":
            v = source_event.get("GAME_ID") or source_event.get("game_id")
            return str(v) if v is not None else None
        return None

    def map_timestamp(self, source_event: Dict[str, Any]) -> datetime:
        ts = source_event.get("ACTIVITY_TS") or source_event.get("activity_ts") or source_event.get("timestamp")
        if isinstance(ts, datetime):
            return ts
        if isinstance(ts, (int, float)):
            if ts > 1e10:
                return datetime.fromtimestamp(ts / 1000)
            return datetime.fromtimestamp(ts)
        if isinstance(ts, str) and ts.strip():
            try:
                return datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except ValueError:
                pass
        return datetime.now()

    def map_properties(self, source_event: Dict[str, Any]) -> Dict[str, Any]:
        props: Dict[str, Any] = {}
        table = (source_event.get("table") or "").lower().strip()

        for k_src, k_out in [
            ("DEVICE_OS", "device_os"),
            ("DEVICE_TYPE", "device_type"),
            ("COUNTRY", "country"),
            ("APPLICATION_VERSION", "app_version"),
        ]:
            if k_src in source_event and source_event.get(k_src) is not None:
                props[k_out] = source_event.get(k_src)

        if table in {"bids", "impressions", "tracker_events"}:
            for k_src, k_out in [
                ("AD_TYPE", "ad_type"),
                ("PLACEMENT_KEY", "placement_key"),
                ("BID_PRICE", "bid_price"),
                ("ACTUAL_REVENUE", "actual_revenue"),
                ("DWELL_TIME", "dwell_time_ms"),
                ("PLAYER_ENGAGEMENT_SCORE", "player_engagement_score"),
            ]:
                if k_src in source_event and source_event.get(k_src) is not None:
                    props[k_out] = source_event.get(k_src)

        props["adinmo_table"] = table or None
        props["adinmo_event_type"] = source_event.get("EVENT_TYPE") or source_event.get("event_type")
        props["adinmo_bid_id"] = source_event.get("BID_ID") or source_event.get("bid_id")
        props["adinmo_impression_id"] = source_event.get("IMPRESSION_ID") or source_event.get("impression_id")
        props["adinmo_campaign_id"] = source_event.get("CAMPAIGN_ID") or source_event.get("campaign_id")
        props["adinmo_image_guid"] = source_event.get("IMAGE_GUID") or source_event.get("image_guid")

        return props



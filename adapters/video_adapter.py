#!/usr/bin/env python3
"""
Video Data Adapter

Processes video data of people playing games and correlates it with gaming data.

Author: Gi Fernando
Copyright: © 2025 Gi Fernando. All rights reserved.
Date: 2025-12-27
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class VideoAdapter:
    """
    Adapter for processing video data of people playing games.
    
    Extracts behavioral cues from video and correlates with game events.
    """
    
    def __init__(self):
        """Initialize the video adapter."""
        pass
    
    def process_video_frame(self, frame_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single video frame to extract behavioral cues.
        
        Args:
            frame_data: Video frame data dictionary with:
                - frame_number: int
                - timestamp: float (seconds in video)
                - image_path: str (path to frame image)
                - detected_emotions: List[Dict] (emotion detection results)
                - detected_actions: List[Dict] (action detection results)
                
        Returns:
            Processed frame data in universal format:
            {
                "frame_id": str,
                "timestamp": float,
                "detected_emotion": str,
                "detected_action": str,
                "video_quality_score": float
            }
        """
        processed_frame = {
            "frame_id": f"frame_{frame_data.get('frame_number', 0)}",
            "timestamp": frame_data.get("timestamp", 0.0),
            "detected_emotion": self._extract_emotion(frame_data),
            "detected_action": self._extract_action(frame_data),
            "video_quality_score": self._calculate_quality_score(frame_data)
        }
        
        return processed_frame
    
    def correlate_with_game_events(
        self,
        video_frames: List[Dict[str, Any]],
        game_events: List[Dict[str, Any]],
        tolerance_seconds: float = 2.0
    ) -> List[Dict[str, Any]]:
        """
        Correlate video frames with game events by timestamp.
        
        Args:
            video_frames: List of processed video frames
            game_events: List of game events with timestamps
            tolerance_seconds: Time tolerance for correlation (default 2.0 seconds)
            
        Returns:
            List of correlated events:
            {
                "video_frame": Dict,
                "game_event": Dict,
                "correlation_score": float,
                "time_difference": float
            }
        """
        correlated_events = []
        
        for frame in video_frames:
            frame_timestamp = frame.get("timestamp", 0.0)
            
            # Find closest game event
            closest_event = None
            min_time_diff = float('inf')
            
            for game_event in game_events:
                game_timestamp = self._extract_game_event_timestamp(game_event)
                if game_timestamp is None:
                    continue
                
                time_diff = abs(frame_timestamp - game_timestamp)
                if time_diff < min_time_diff and time_diff <= tolerance_seconds:
                    min_time_diff = time_diff
                    closest_event = game_event
            
            if closest_event:
                correlation_score = 1.0 - (min_time_diff / tolerance_seconds)
                correlated_events.append({
                    "video_frame": frame,
                    "game_event": closest_event,
                    "correlation_score": correlation_score,
                    "time_difference": min_time_diff
                })
        
        return correlated_events
    
    def extract_behavioral_patterns(
        self,
        correlated_events: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Extract behavioral patterns from correlated video and game events.
        
        Args:
            correlated_events: List of correlated video/game events
            
        Returns:
            Behavioral patterns dictionary:
            {
                "emotion_patterns": Dict,
                "action_patterns": Dict,
                "engagement_indicators": List,
                "frustration_indicators": List
            }
        """
        patterns = {
            "emotion_patterns": {},
            "action_patterns": {},
            "engagement_indicators": [],
            "frustration_indicators": []
        }
        
        for correlated in correlated_events:
            frame = correlated["video_frame"]
            game_event = correlated["game_event"]
            
            # Extract emotion patterns
            emotion = frame.get("detected_emotion")
            if emotion:
                if emotion not in patterns["emotion_patterns"]:
                    patterns["emotion_patterns"][emotion] = []
                patterns["emotion_patterns"][emotion].append({
                    "game_event_type": game_event.get("event_type"),
                    "timestamp": frame.get("timestamp")
                })
            
            # Extract action patterns
            action = frame.get("detected_action")
            if action:
                if action not in patterns["action_patterns"]:
                    patterns["action_patterns"][action] = []
                patterns["action_patterns"][action].append({
                    "game_event_type": game_event.get("event_type"),
                    "timestamp": frame.get("timestamp")
                })
            
            # Engagement indicators
            if emotion in ["happy", "excited", "concentrated"]:
                patterns["engagement_indicators"].append({
                    "timestamp": frame.get("timestamp"),
                    "game_event": game_event.get("event_type")
                })
            
            # Frustration indicators
            if emotion in ["frustrated", "angry", "confused"]:
                patterns["frustration_indicators"].append({
                    "timestamp": frame.get("timestamp"),
                    "game_event": game_event.get("event_type")
                })
        
        return patterns
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def _extract_emotion(self, frame_data: Dict[str, Any]) -> Optional[str]:
        """Extract primary emotion from frame data."""
        detected_emotions = frame_data.get("detected_emotions", [])
        if not detected_emotions:
            return None
        
        # Return emotion with highest confidence
        best_emotion = max(
            detected_emotions,
            key=lambda e: e.get("confidence", 0.0)
        )
        return best_emotion.get("emotion")
    
    def _extract_action(self, frame_data: Dict[str, Any]) -> Optional[str]:
        """Extract primary action from frame data."""
        detected_actions = frame_data.get("detected_actions", [])
        if not detected_actions:
            return None
        
        # Return action with highest confidence
        best_action = max(
            detected_actions,
            key=lambda a: a.get("confidence", 0.0)
        )
        return best_action.get("action")
    
    def _calculate_quality_score(self, frame_data: Dict[str, Any]) -> float:
        """Calculate video quality score (0.0 to 1.0)."""
        # Simple quality score based on available data
        score = 0.5  # Base score
        
        # Increase score if emotions detected
        if frame_data.get("detected_emotions"):
            score += 0.2
        
        # Increase score if actions detected
        if frame_data.get("detected_actions"):
            score += 0.2
        
        # Increase score if image quality is good
        image_quality = frame_data.get("image_quality", 0.5)
        score += image_quality * 0.1
        
        return min(score, 1.0)
    
    def _extract_game_event_timestamp(self, game_event: Dict[str, Any]) -> Optional[float]:
        """Extract timestamp from game event."""
        timestamp = game_event.get("activity_timestamp")
        if timestamp is None:
            return None
        
        # Convert datetime to float timestamp
        if isinstance(timestamp, datetime):
            return timestamp.timestamp()
        elif isinstance(timestamp, (int, float)):
            return float(timestamp)
        elif isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                return dt.timestamp()
            except ValueError:
                return None
        
        return None


if __name__ == "__main__":
    # Example usage
    adapter = VideoAdapter()
    
    # Example video frame
    frame_data = {
        "frame_number": 100,
        "timestamp": 10.5,
        "detected_emotions": [
            {"emotion": "happy", "confidence": 0.85},
            {"emotion": "excited", "confidence": 0.60}
        ],
        "detected_actions": [
            {"action": "smiling", "confidence": 0.80}
        ]
    }
    
    # Process frame
    processed_frame = adapter.process_video_frame(frame_data)
    print(json.dumps(processed_frame, indent=2))


# =============================
# core/composio_utils.py
# Utility functions for composio integration or features
# =============================

import logging
from composio_openai import ComposioToolSet, Action

logger = logging.getLogger(__name__)

def get_place_details(place_name):
    """
    Fetch detailed information about a place using Composio's Google Maps agent.
    """
    try:
        toolset = ComposioToolSet()
        result = toolset.execute_action(
            action=Action.GOOGLEMAPS_GET_PLACE_INFO,
            params={
            "place_name": place_name
        }
        )
        
        if not result.get("successful"):
            return {"error": result.get("error", "Failed to fetch place details")}
            
        return result.get("data", {})
    except Exception as e:
        logger.error(f"Error fetching place details: {str(e)}")
        return {"error": f"Failed to fetch place details: {str(e)}"}

def get_route_planning(origin, destination, mode="driving"):
    """
    Get route planning information between two locations.
    """
    try:
        toolset = ComposioToolSet()
        result = toolset.execute_action(
            action=Action.GOOGLEMAPS_GET_DIRECTIONS,
            params={
            "origin": origin,
            "destination": destination,
                "mode": mode
            }
        )
        
        if not result.get("successful"):
            return {"error": result.get("error", "Failed to fetch route planning")}
            
        return result.get("data", {})
    except Exception as e:
        logger.error(f"Error fetching route planning: {str(e)}")
        return {"error": f"Failed to fetch route planning: {str(e)}"} 
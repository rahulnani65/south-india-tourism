import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_place_details(place_name):
    """
    Fetch detailed information about a place using Composio's Google Maps agent.
    """
    try:
        # Updated Composio API endpoint
        url = 'https://api.composio.dev/v1/agents/invoke'
        
        headers = {
            'Authorization': f'Bearer {settings.COMPOSIO_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        payload = {
            "agent_id": "google-maps-agent",  # Specify the agent ID
            "action": "get_place_info",
            "parameters": {
                "place_name": place_name
            }
        }
        
        logger.info(f"Making request to Composio API for place: {place_name}")
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Successfully received response from Composio API")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching place details: {str(e)}")
        return {"error": f"Failed to fetch place details: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error in get_place_details: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}

def get_route_planning(origin, destination, mode="driving"):
    """
    Get route planning information between two locations.
    """
    try:
        # Updated Composio API endpoint
        url = 'https://api.composio.dev/v1/agents/invoke'
        
        headers = {
            'Authorization': f'Bearer {settings.COMPOSIO_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        payload = {
            "agent_id": "google-maps-agent",  # Specify the agent ID
            "action": "get_directions",
            "parameters": {
                "origin": origin,
                "destination": destination,
                "mode": mode  # driving, walking, bicycling, transit
            }
        }
        
        logger.info(f"Making request to Composio API for route from {origin} to {destination}")
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Successfully received response from Composio API")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching route planning: {str(e)}")
        return {"error": f"Failed to fetch route planning: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error in get_route_planning: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"} 
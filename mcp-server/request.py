from typing import Dict, Any, Optional, Union
import httpx
import logging

FORTUNA_API_BASE = "http://localhost:8000"
FORTUNA_API_KEY = ""


logger = logging.getLogger(__name__)

async def fortuna_request(
    endpoint: str, 
    method: str = "GET",
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Make a request to the Fortuna Flow API with proper error handling.
    
    Args:
        endpoint: API endpoint path (without base URL)
        method: HTTP method (GET, POST, PUT, DELETE)
        data: JSON data to send in request body (for POST, PUT)
        params: Query parameters for the request
    
    Returns:
        Response JSON data or None if error occurs
    """
    url = f"{FORTUNA_API_BASE}/api/{endpoint}"
    headers = {
        "Authorization": f"Bearer {FORTUNA_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            request_kwargs = {
                "url": url,
                "headers": headers,
                "timeout": 30.0
            }
            
            if params:
                request_kwargs["params"] = params
            
            if method.upper() in ["POST", "PUT"] and data:
                request_kwargs["json"] = data
            
            if method.upper() == "GET":
                response = await client.get(**request_kwargs)
            elif method.upper() == "POST":
                response = await client.post(**request_kwargs)
            elif method.upper() == "PUT":
                response = await client.put(**request_kwargs)
            elif method.upper() == "DELETE":
                response = await client.delete(**request_kwargs)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            logger.info(f"Request to {endpoint} successful - Status: {response.status_code}")
            
            if response.content:
                return response.json()
            return {}
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None


async def fortuna_get(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """GET request to Fortuna API"""
    return await fortuna_request(endpoint, "GET", params=params)


async def fortuna_post(endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """POST request to Fortuna API"""
    return await fortuna_request(endpoint, "POST", data=data, params=params)


async def fortuna_put(endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """PUT request to Fortuna API"""
    return await fortuna_request(endpoint, "PUT", data=data, params=params)


async def fortuna_delete(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """DELETE request to Fortuna API"""
    return await fortuna_request(endpoint, "DELETE", params=params)

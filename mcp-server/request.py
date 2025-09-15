import json
import httpx
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class FortunaClient:
    def __init__(self, api_key: str, api_base: str) -> None:
        """
        Fortuna API Client

        Args:
            api_key: API key for authentication
            api_base: Base URL of the Fortuna API (e.g. "https://example.com")
        """
        self.api_key = api_key
        self.api_base = api_base.rstrip("/")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def _request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Internal request handler."""
        url = f"{self.api_base}/api/{endpoint.lstrip('/')}"

        async with httpx.AsyncClient() as client:
            try:
                request_kwargs = {
                    "url": url,
                    "headers": self.headers,
                    "timeout": 30.0,
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
                    return json.dumps(response.json())
                return "No Data"

            except httpx.HTTPStatusError as e:
                return f"HTTP error {e.response.status_code}: {e.response.text}"
            except httpx.RequestError as e:
                return f"Request error: {e}"
            except Exception as e:
                return f"Unexpected error: {e}"

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        return await self._request(endpoint, "GET", params=params)

    async def post(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        return await self._request(endpoint, "POST", data=data, params=params)

    async def put(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        return await self._request(endpoint, "PUT", data=data, params=params)

    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        return await self._request(endpoint, "DELETE", params=params)

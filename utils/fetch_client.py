"""
HTTP client utility for external service integration
"""
import httpx  # type: ignore[import-untyped]
from typing import Any, Optional, Dict
import logging

logger = logging.getLogger(__name__)


class APIClient:
    """
    Unified HTTP client for external service integration
    
    Provides standardized HTTP methods with automatic JSON handling,
    error management, and timeout configuration.
    """
    
    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30
    ) -> None:
        """
        Initialize API client
        
        Args:
            base_url: Base URL for the API
            headers: Default headers to include in all requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout
        )
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            files: Files to upload
            **kwargs: Additional request arguments
            
        Returns:
            Response JSON data or None on error
        """
        try:
            url = f"{self.base_url}{endpoint}" if not endpoint.startswith('http') else endpoint
            
            request_kwargs = {
                "params": params,
                **kwargs
            }
            
            if files:
                request_kwargs["files"] = files
            elif data and method.upper() in ["POST", "PUT", "PATCH"]:
                request_kwargs["json"] = data
            
            response = await self.client.request(
                method=method.upper(),
                url=url,
                **request_kwargs
            )
            
            response.raise_for_status()
            
            if response.headers.get("content-type", "").startswith("application/json"):
                json_data = response.json()
                if isinstance(json_data, dict):
                    return json_data
                return {"data": json_data}
            return {"status": response.status_code, "content": response.text}
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None
    
    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Make GET request"""
        return await self._request("GET", endpoint, params=params, **kwargs)
    
    async def post(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        files: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Make POST request"""
        return await self._request("POST", endpoint, data=data, files=files, **kwargs)
    
    async def put(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Make PUT request"""
        return await self._request("PUT", endpoint, data=data, **kwargs)
    
    async def delete(
        self,
        endpoint: str,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Make DELETE request"""
        return await self._request("DELETE", endpoint, **kwargs)
    
    async def patch(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Make PATCH request"""
        return await self._request("PATCH", endpoint, data=data, **kwargs)
    
    async def close(self) -> None:
        """Close the HTTP client"""
        await self.client.aclose()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import asyncio
        asyncio.run(self.close())
    
    # Synchronous methods for backward compatibility
    def get_sync(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Make synchronous GET request"""
        import asyncio
        return asyncio.run(self.get(endpoint, params=params, **kwargs))
    
    def post_sync(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        files: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Make synchronous POST request"""
        import asyncio
        return asyncio.run(self.post(endpoint, data=data, files=files, **kwargs))


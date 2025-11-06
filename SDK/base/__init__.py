"""
Base SDK client for external service integration
"""
from SDK.base.resource import Resource
from utils.fetch_client import APIClient
from typing import Any
from config import general_config


class BaseClient:
    """
    BaseClient is the main entry point for interacting with external microservices.
    """
    
    def __init__(self) -> None:
        self.client = APIClient(
            base_url=general_config.BASE_API_BASE_URL if hasattr(general_config, 'BASE_API_BASE_URL') else "",
            headers={
                "Content-Type": "application/json",
                "X-Api-Key": general_config.BASE_API_KEY if hasattr(general_config, 'BASE_API_KEY') else "",
            },
        )
        self.resource = Resource(self.client)
        
    async def test_service(self) -> dict[str, Any] | None:
        """
        Sends a test request to the Base API to verify connectivity.
        :return: API response JSON or None on error.
        """
        return await self.client.get("/")


base_client = BaseClient()


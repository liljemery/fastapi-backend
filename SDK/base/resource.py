"""
Resource module for Base SDK
"""
from utils.fetch_client import APIClient
from typing import Any, Dict, Optional
from common.exceptions.sdk import (
    SDKException,
    SDKResourceNotFoundError,
    SDKValidationError
)
import logging

logger = logging.getLogger(__name__)


class Resource:
    """
    Resource operations for Base SDK
    
    """
    
    def __init__(self, client: APIClient):
        self.client = client
        self.logger = logging.getLogger(f"{__name__}.Resource")
    
    async def get_resource(self, resource_id: str) -> Dict[str, Any]:
        """
        Get a resource by ID
        
        Args:
            resource_id: Resource identifier
            
        Returns:
            Resource data
            
        Raises:
            SDKResourceNotFoundError: If resource doesn't exist
            SDKException: For other API errors
        """
        if not resource_id:
            raise SDKValidationError("resource_id is required")
        
        self.logger.debug(f"Fetching resource: {resource_id}")
        
        response = await self.client.get(f"/resources/{resource_id}")
        
        if response is None:
            raise SDKResourceNotFoundError(f"Resource {resource_id} not found")
        
        self.logger.info(f"Successfully fetched resource: {resource_id}")
        return response
    
    async def create_resource(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new resource
        
        Args:
            data: Resource data
            
        Returns:
            Created resource data
            
        Raises:
            SDKValidationError: If data is invalid
            SDKException: For other API errors
        """
        if not data:
            raise SDKValidationError("data is required")
        
        self.logger.debug(f"Creating resource with data: {data}")
        
        response = await self.client.post("/resources/", data=data)
        
        if response is None:
            raise SDKException("Failed to create resource")
        
        self.logger.info(f"Successfully created resource: {response.get('id', 'unknown')}")
        return response
    
    async def update_resource(self, resource_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a resource
        
        Args:
            resource_id: Resource identifier
            data: Updated resource data
            
        Returns:
            Updated resource data
            
        Raises:
            SDKResourceNotFoundError: If resource doesn't exist
            SDKValidationError: If data is invalid
            SDKException: For other API errors
        """
        if not resource_id:
            raise SDKValidationError("resource_id is required")
        if not data:
            raise SDKValidationError("data is required")
        
        self.logger.debug(f"Updating resource {resource_id} with data: {data}")
        
        response = await self.client.put(f"/resources/{resource_id}", data=data)
        
        if response is None:
            raise SDKResourceNotFoundError(f"Resource {resource_id} not found or update failed")
        
        self.logger.info(f"Successfully updated resource: {resource_id}")
        return response
    
    async def delete_resource(self, resource_id: str) -> Dict[str, Any]:
        """
        Delete a resource
        
        Args:
            resource_id: Resource identifier
            
        Returns:
            Deletion result
            
        Raises:
            SDKResourceNotFoundError: If resource doesn't exist
            SDKException: For other API errors
        """
        if not resource_id:
            raise SDKValidationError("resource_id is required")
        
        self.logger.debug(f"Deleting resource: {resource_id}")
        
        response = await self.client.delete(f"/resources/{resource_id}")
        
        if response is None:
            raise SDKResourceNotFoundError(f"Resource {resource_id} not found or delete failed")
        
        self.logger.info(f"Successfully deleted resource: {resource_id}")
        return response
    
    async def list_resources(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List all resources
        
        Args:
            params: Query parameters (pagination, filters, etc.)
            
        Returns:
            List of resources with pagination metadata
            
        Raises:
            SDKException: For API errors
        """
        self.logger.debug(f"Listing resources with params: {params}")
        
        response = await self.client.get("/resources/", params=params)
        
        if response is None:
            raise SDKException("Failed to list resources")
        
        resource_count = len(response.get("items", []))
        self.logger.info(f"Successfully listed {resource_count} resources")
        return response


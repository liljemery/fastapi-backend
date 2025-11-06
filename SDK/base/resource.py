"""
Resource module for Base SDK
"""
from utils.fetch_client import APIClient
from typing import Any, Optional, Dict


class Resource:
    """
    Resource operations for Base SDK
    """
    
    def __init__(self, client: APIClient):
        self.client = client
    
    async def get_resource(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a resource by ID
        
        Args:
            resource_id: Resource identifier
            
        Returns:
            Resource data or None on error
        """
        try:
            response = await self.client.get(f"/resources/{resource_id}")
            return response
        except Exception as e:
            print(f"Error fetching resource: {e}")
            return None
    
    async def create_resource(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new resource
        
        Args:
            data: Resource data
            
        Returns:
            Created resource data or None on error
        """
        try:
            response = await self.client.post("/resources/", data=data)
            return response
        except Exception as e:
            print(f"Error creating resource: {e}")
            return None
    
    async def update_resource(self, resource_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a resource
        
        Args:
            resource_id: Resource identifier
            data: Updated resource data
            
        Returns:
            Updated resource data or None on error
        """
        try:
            response = await self.client.put(f"/resources/{resource_id}", data=data)
            return response
        except Exception as e:
            print(f"Error updating resource: {e}")
            return None
    
    async def delete_resource(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """
        Delete a resource
        
        Args:
            resource_id: Resource identifier
            
        Returns:
            Deletion result or None on error
        """
        try:
            response = await self.client.delete(f"/resources/{resource_id}")
            return response
        except Exception as e:
            print(f"Error deleting resource: {e}")
            return None
    
    async def list_resources(self, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        List all resources
        
        Args:
            params: Query parameters
            
        Returns:
            List of resources or None on error
        """
        try:
            response = await self.client.get("/resources/", params=params)
            return response
        except Exception as e:
            print(f"Error listing resources: {e}")
            return None


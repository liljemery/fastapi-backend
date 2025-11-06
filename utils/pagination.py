"""
Pagination utilities
"""
from typing import TypeVar, Generic, List
from pydantic import BaseModel  # type: ignore[import-untyped]

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    class Config:
        arbitrary_types_allowed = True


def paginate(query, page: int = 1, page_size: int = 10):
    """
    Paginate a SQLAlchemy query
    
    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        page_size: Items per page
        
    Returns:
        PaginatedResponse
    """
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


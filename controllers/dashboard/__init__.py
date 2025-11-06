"""
Dashboard controllers
"""
from fastapi import Request  # type: ignore[import]
from common.exceptions.dashboard import UserNotFoundError
from common.exceptions.session import NoSessionError
from database import SessionLocal, close_session
from services.dashboard import dashboard_services
from fastapi.responses import JSONResponse  # type: ignore[import]
from sqlmodel import Session
from typing import cast


async def get_dashboard_info_controller(request: Request) -> JSONResponse:
    """
    Get dashboard information for the authenticated user
    
    Args:
        request: FastAPI request object
        
    Returns:
        JSONResponse with user dashboard data
    """
    try:
        session = cast(Session, SessionLocal())
        try:
            user = dashboard_services.get_user_by_uuid(
                user_uuid=request.state.user_uuid, session=session
            )
            
            return JSONResponse(
                status_code=200,
                content={
                    "user": {
                        "id": user.id,
                        "uuid": user.uuid,
                        "email": user.email,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "is_active": user.is_active,
                        "is_admin": user.is_admin,
                        "is_verified": user.is_verified,
                        "created_at": user.created_at.isoformat() if user.created_at else None,
                        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                    }
                },
            )
        finally:
            close_session(session)
    except UserNotFoundError as e:
        return JSONResponse(status_code=404, content={"message": e.message})
    except NoSessionError as e:
        return JSONResponse(
            status_code=500, content={"message": f"Session error: {str(e)}"}
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500, content={"error": f"Unexpected error: {str(e)}"}
        )


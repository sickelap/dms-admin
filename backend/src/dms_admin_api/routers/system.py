from fastapi import APIRouter, Depends

from dms_admin_api.auth import require_authenticated_user
from dms_admin_api.config import Settings, get_settings
from dms_admin_api.dms.service import DmsService, get_dms_service
from dms_admin_api.schemas import SystemStateResponse

router = APIRouter(prefix="/system", tags=["system"])

@router.get("/status", response_model=SystemStateResponse)
def system_status(
    _: str = Depends(require_authenticated_user),
    settings: Settings = Depends(get_settings),
    dms: DmsService = Depends(get_dms_service),
) -> SystemStateResponse:
    return SystemStateResponse(
        dms_container_name=settings.dms_container_name,
        dms_reachable=dms.connectivity(),
    )

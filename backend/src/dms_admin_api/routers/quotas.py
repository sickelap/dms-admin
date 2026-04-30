from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from dms_admin_api.auth import require_authenticated_user
from dms_admin_api.dms.models import MutationResult, Quota
from dms_admin_api.dms.service import DmsService, get_dms_service

router = APIRouter(prefix="/quotas", tags=["quotas"])


class SetQuotaRequest(BaseModel):
    email: EmailStr
    quota: str


@router.get("", response_model=list[Quota])
def list_quotas(
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> list[Quota]:
    return dms.list_quotas()


@router.post("", response_model=MutationResult)
def set_quota(
    payload: SetQuotaRequest,
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> MutationResult:
    return dms.set_quota(email=str(payload.email), quota=payload.quota)


@router.delete("/{email}", response_model=MutationResult)
def delete_quota(
    email: EmailStr,
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> MutationResult:
    return dms.delete_quota(email=str(email))

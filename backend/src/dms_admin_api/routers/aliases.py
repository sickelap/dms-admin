from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, EmailStr

from dms_admin_api.auth import require_authenticated_user
from dms_admin_api.dms.models import Alias, MutationResult
from dms_admin_api.dms.service import DmsService, get_dms_service

router = APIRouter(prefix="/aliases", tags=["aliases"])


class CreateAliasRequest(BaseModel):
    address: EmailStr
    target: EmailStr


@router.get("", response_model=list[Alias])
def list_aliases(
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> list[Alias]:
    return dms.list_aliases()


@router.post("", response_model=MutationResult)
def create_alias(
    payload: CreateAliasRequest,
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> MutationResult:
    return dms.create_alias(address=str(payload.address), target=str(payload.target))


@router.delete("/{address}", response_model=MutationResult)
def delete_alias(
    address: EmailStr,
    target: EmailStr = Query(...),
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> MutationResult:
    return dms.delete_alias(address=str(address), target=str(target))

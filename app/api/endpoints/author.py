from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.model.model import Author
from app.schema.author import CreateAuthor, UpdateAuthor, GetAuthorRequest
from app.schema.base import CommonSuccessResponse

from app.service.author_service import AuthorService

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.get("/{id}")
@inject
async def get_by_id(id: int, service: AuthorService = Depends(Provide[Container.author_service])):
    return service.get_by_id(id)

@router.get("/")
@inject
async def get(req: GetAuthorRequest = Depends(), service: AuthorService = Depends(Provide[Container.author_service])):
    return service.get(req)


@router.post("/")
@inject
async def create(req: CreateAuthor, service: AuthorService = Depends(Provide[Container.author_service])):
    return service.create(req)

@router.put("/{id}")
@inject
async def update(id: int, req: UpdateAuthor, service: AuthorService = Depends(Provide[Container.author_service])):
    req.id = id
    return service.update(req)

@router.delete("/{id}")
@inject
async def delete(id: int, service: AuthorService = Depends(Provide[Container.author_service])):
    service.delete(id)

    return CommonSuccessResponse()

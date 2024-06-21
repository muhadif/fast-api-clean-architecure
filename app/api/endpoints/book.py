from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.model.model import Book
from app.schema.book import CreateBook, UpdateBook, GetBookRequest
from app.schema.base import CommonSuccessResponse

from app.service.book_service import BookService

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get("/{id}")
@inject
async def get_by_id(id: int, service: BookService = Depends(Provide[Container.book_service])):
    return service.get_by_id(id)

@router.get("/")
@inject
async def get(req: GetBookRequest = Depends(), service: BookService = Depends(Provide[Container.book_service])):
    return service.get(req)


@router.post("/")
@inject
async def create(req: CreateBook, service: BookService = Depends(Provide[Container.book_service])):
    return service.create(req)

@router.put("/{id}")
@inject
async def update(id: int, req: UpdateBook, service: BookService = Depends(Provide[Container.book_service])):
    req.id = id
    return service.update(req)

@router.delete("/{id}")
@inject
async def delete(id: int, service: BookService = Depends(Provide[Container.book_service])):
    service.delete(id)

    return CommonSuccessResponse()

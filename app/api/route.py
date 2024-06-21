from fastapi import APIRouter

from app.api.endpoints.author import router as author_router
from app.api.endpoints.book import router as book_router

routers = APIRouter()
router_list = [author_router, book_router]

for router in router_list:
    router.tags = routers
    routers.include_router(router)
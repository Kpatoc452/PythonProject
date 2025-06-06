from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .product import router as product_router
from .category import router as category_router
from .purchase import router as purchase_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(product_router)
router.include_router(category_router)
router.include_router(purchase_router)
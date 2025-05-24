from .base import BaseCRUD
from core.models import Category

class CategoryCRUD(BaseCRUD):
    model = Category
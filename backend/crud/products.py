from .base import BaseCRUD
from core.models import Product

class ProductCRUD(BaseCRUD):
    model = Product 
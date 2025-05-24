from .base import BaseCRUD
from core.models import Purchase

class PurchaseCRUD(BaseCRUD):
    model = Purchase